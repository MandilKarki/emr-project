# import openai
# import configparser
#
#
# # import the path to the configuration file from the config module
# # import the path to the configuration file from the config module
# from config import CONFIG_FILE_PATH
#
#
# # read the API key from the configuration file
# with open(CONFIG_FILE_PATH, "r") as config_file:
#     config = configparser.ConfigParser()
#     config.read_file(config_file)
#     api_key = config["openai"]["api_key"]
#
# openai.api_key = api_key  # set the API key
#
# # define the prompt and EMR text
# prompt = """
# Please extract the following information from the following electronic medical record (EMR):
# - Patient's age
# - Patient's gender
# - Patient's diagnoses
#
# EMR text:
# """
#
# emr_text = """
# Patient Name: John Doe
# Date of Birth: 01/01/1970
#
# Medical History:
# - Hypertension
# - Type 2 diabetes
# - Coronary artery disease
#
# Chief Complaint: Chest pain
#
# Assessment and Plan:
# - Obtain an ECG and cardiac enzymes
# - Administer aspirin and nitroglycerin
# - Consult with cardiology for further management
#
# Medications:
# - Lisinopril 20 mg orally once daily
# - Metformin 1000 mg orally twice daily
# - Aspirin 81 mg orally once daily
#
# Follow-up:
# - Follow-up with cardiology in 3 days
# - Follow-up with primary care in 1 week
# """
#
#
# # append the EMR text to the prompt
# prompt += emr_text
#
# # call the OpenAI API
# try:
#     completion = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         max_tokens=1024,
#         temperature=0.5,
#         top_p=1,
#         frequency_penalty=1,
#         presence_penalty=1
#     )
# except Exception as e:
#     print("The OpenAI API request failed:", e)
#
# # retrieve the generated text from the completion object
# completion_text = completion["choices"][0]["text"]
#
# # print the generated text
# print(completion_text)

'''
Here are 10 entities that may be present in an electronic medical record (EMR):

    Patient's name
    Patient's age
    Patient's gender
    Patient's diagnoses
    Patient's medications
    Patient's allergies
    Patient's vital signs (e.g. blood pressure, heart rate, temperature)
    Patient's laboratory test results
    Patient's past medical history
    Referral information (e.g. referral to another healthcare provider)
'''
# openai.py
import openai
import configparser
import re
from config import CONFIG_FILE_PATH

# emr_prompt = """
# Please extract the following information from the following electronic medical record (EMR):
# - Patient's age
# - Patient's gender
# - Patient's diagnoses
# - Patient's medications
# - Patient's allergies
# - Patient's vital signs (e.g. blood pressure, heart rate, etc.)
# - Patient's test results (e.g. lab test results, imaging test results, etc.)
# - Patient's past medical history
# - Patient's family medical history
# - Patient's social history (e.g. smoking, alcohol use, etc.)
#
# EMR text:
# """
emr_prompt = """ 
Please extract the following entities
1 Patient's age:
2 Patient's gender:
3 Patient's diagnoses:
4 Patient's medications:
5 Patient's allergies:
6 Patient's vital signs:
7 Patient's test results:
8 Patient's past medical history:

  
for example- 
emr1 = Patient is a 25 year old female with a diagnosis of asthma. She is currently taking Albuterol and Fluticasone inhalers for her symptoms. 
She has no known allergies. Her vital signs today include a blood pressure of 120/80 mmHg and a heart rate of 70 bpm. 
She has recently had a chest x-ray, the results of which were normal. She has a history of eczema and her mother has a history of hypertension.
 The patient does not smoke or drink alcohol.
the entities extracted are - 
1 Patient's age: 25
2 Patient's gender: female
3 Patient's diagnoses: asthma
4 Patient's medications: Albuterol, Fluticasone inhalers
5 Patient's allergies: None
6 Patient's vital signs: blood pressure 120/80 mmHg, heart rate 70 bpm
7 Patient's test results: chest x-ray normal
8 Patient's past medical history: eczema


"""


def initialize_openai_client(config_file_path):
    # read the API key from the configuration file
    with open(config_file_path, "r") as config_file:
        config = configparser.ConfigParser()
        config.read_file(config_file)
        api_key = config["openai"]["api_key"]

    openai.api_key = api_key
    api_key = openai.api_key# set the API key
    return api_key


api_key = initialize_openai_client(CONFIG_FILE_PATH)



def generate_text_completion( emr_text: str):
    # call the OpenAI API
    completion = openai.Completion.create(
        engine="text-davinci-001",
        prompt=emr_prompt+emr_text,
        max_tokens=1200,
        temperature=0.4,
        api_key=api_key,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
    )

    if completion is None:
        raise Exception("The OpenAI API request failed")

    completion_text = completion["choices"][0]["text"]

    return completion_text


def extract_entites(completion_text: str):

    entities = {
        "age": None,
        "gender": None,
        "diagnoses": [],
        "medications": [],
        "allergies": [],
        "vital_signs": [],
        "test_results": [],
        "past_medical_history": [],
        "family_medical_history": [],
        "social_history": []
    }

    if completion_text is not None:
        lines = completion_text.split("\n")
        for line in lines:
            line = line.strip()
            print(line)
            if line.startswith("1 Patient's age:"):
                entities["age"] = line.split(":", 1)[1].strip()
            elif line.startswith("2 Patient's gender:"):
                entities["gender"] = line.split(":", 1)[1].strip()
            elif line.startswith("3 Patient's diagnoses:"):
                diagnoses = line.split(":", 1)[1].strip()
                entities["diagnoses"] = re.split(r",\s*", diagnoses)
            elif line.startswith("4 Patient's medications:"):
                medications = line.split(":", 1)[1].strip()
                entities["medications"] = re.split(r",\s*", medications)
            elif line.startswith("5 Patient's allergies:"):
                allergies = line.split(":", 1)[1].strip()
                entities["allergies"] = re.split(r",\s*", allergies)
            elif line.startswith("6 Patient's vital signs:"):
                vital_signs = line.split(":", 1)[1].strip()
                entities["vital_signs"] = re.split(r",\s*", vital_signs)
            elif line.startswith("7 Patient's test results:"):
                test_results = line.split(":", 1)[1].strip()
                entities["test_results"] = re.split(r",\s*", test_results)
            elif line.startswith("8 Patient's past medical history:"):
                past_medical_history = line.split(":", 1)[1].strip()
                entities["past_medical_history"] = re.split(r",\s*", past_medical_history)
            elif line.startswith("Patient's family medical history:"):
                family_medical_history = line.split(":", 1)[1].strip()
                entities["family_medical_history"] = re.split(r",\s*", family_medical_history)
            elif line.startswith("Patient's social history:"):
                social_history = line.split(":", 1)[1].strip()
                entities["social_history"] = re.split(r",\s*", social_history)
    elif completion_text["choices"][0]["text"] is None:
        return "no entities were extracted"

    return entities


'''experimentation'''

emr_text = '''em2 = Patient is a 37 year old male with a diagnosis of type 2 diabetes mellitus. He is taking Metformin and Januvia for his
condition. He has a known allergy to penicillin. His vital signs today include a blood pressure of 130/85 mmHg and a heart rate of 75 bpm.
He has recently had a hemoglobin A1c test, the result of which was 7.5%. He has a history of obesity and his father has 
a history of myocardial infarction. The patient is a current smoker and drinks alcohol occasionally. 
the entities extracted are - 

 '''
from config import CONFIG_FILE_PATH

# initialize_openai_client(CONFIG_FILE_PATH)
# completion_text = generate_text_completion(emr_prompt, emr_text)
# ent = extract_entites(completion_text)
# print(ent)