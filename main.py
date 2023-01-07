from fastapi import FastAPI


# import the initialize_openai_client and generate_text_completion functions from the openai module
from one_shot_prompt import initialize_openai_client, generate_text_completion, extract_entites

# import the path to the configuration file and the one_shot_prompt function from the prompts module
from config import CONFIG_FILE_PATH

initialize_openai_client(CONFIG_FILE_PATH)  # initialize the OpenAI client

app = FastAPI()


@app.post("/emr_extraction")
def generate_text_completions(emr_text: str):
    try:
        # call the one_shot_prompt function
        completion_text = generate_text_completion(emr_text)
        completion_text = extract_entites(completion_text)
    except Exception as e:
        return {"error": str(e)}
    return {"completion_text": completion_text}

