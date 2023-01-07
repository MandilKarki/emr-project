import openai
import re

'''
EMR text:
Patient is a 25 year old female with a diagnosis of asthma. She is currently taking Albuterol and Fluticasone inhalers for her symptoms. 
She has no known allergies. Her vital signs today include a blood pressure of 120/80 mmHg and a heart rate of 70 bpm. 
She has recently had a chest x-ray, the results of which were normal. She has a history of eczema and her mother has a history of hypertension.
 The patient does not smoke or drink alcohol.

EMR text:
Patient is a 37 year old male with a diagnosis of type 2 diabetes mellitus. He is taking Metformin and Januvia for his
condition. He has a known allergy to penicillin. His vital signs today include a blood pressure of 130/85 mmHg and a heart rate of 75 bpm.
He has recently had a hemoglobin A1c test, the result of which was 7.5%. He has a history of obesity and his father has 
a history of myocardial infarction. The patient is a current smoker and drinks alcohol occasionally.

EMR text:
Patient is a 52 year old female with a diagnosis of hypertension. She is taking Lisinopril and Hydrochlorothiazide for her condition.
 She has no known allergies. Her vital signs today include a blood pressure of 140/90 mmHg and a heart rate of 80 bpm. 
 She has recently had a lipid panel, the results of which were within normal limits. She has a history of migraines and
  her mother has a history of breast cancer. The patient does not smoke but drinks alcohol occasionally.
  
EMR text:
"Patient is experiencing fever, cough, and body aches. They have been prescribed antibiotics and advised to rest at home. 
The patient has a history of asthma, but it is unclear if the current symptoms are related."
'''
'''
Patient 1

    Patient's age: 25
    Patient's gender: female
    Patient's diagnoses: asthma
    Patient's medications: Albuterol, Fluticasone inhalers
    Patient's allergies: None
    Patient's vital signs: blood pressure 120/80 mmHg, heart rate 70 bpm
    Patient's test results: chest x-ray normal
    Patient's past medical history: eczema
    Patient's family medical history: mother has hypertension
    Patient's social history: does not smoke, does not drink alcohol

Patient 2

    Patient's age: 37
    Patient's gender: male
    Patient's diagnoses: type 2 diabetes mellitus
    Patient's medications: Metformin, Januvia
    Patient's allergies: penicillin
    Patient's vital signs: blood pressure 130/85 mmHg, heart rate 75 bpm
    Patient's test results: hemoglobin A1c 7.5%
    Patient's past medical history: obesity
    Patient's family medical history: father has myocardial infarction
    Patient's social history: smokes, drinks alcohol occasionally

Patient 3

    Patient's age: 52
    Patient's gender: female
    Patient's diagnoses: hypertension
    Patient's medications: Lisinopril, Hydrochlorothiazide
    Patient's allergies: None
    Patient's vital signs: blood pressure 140/90 mmHg, heart rate 80 bpm
    Patient's test results: lipid panel normal
    Patient's past medical history: migraines
    Patient's family medical history: mother has breast cancer
    Patient's social history: does not smoke, drinks alcohol occasionally
'''

def initialize_openai_client(api_key):
    openai.api_key = "xxxxxxxxxxxxxxxxxxxxxxxx"


def generate_text_completion(prompt, model, api_key):
    completion = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    return completion if completion is not None else None


def extract_entities(emr_text, api_key):
    # Initialize OpenAI client
    initialize_openai_client(api_key)

    # Define the prompt
    prompt = f"""Please extract the following information from the following electronic medical record (EMR):
- Patient's age
- Patient's gender
- Patient's diagnoses
- Patient's medications
- Patient's allergies
- Patient's vital signs (e.g. blood pressure, heart rate, etc.)
- Patient's test results (e.g. lab test results, imaging test results, etc.)
- Patient's past medical history
- Patient's family medical history
- Patient's social history (e.g. smoking, alcohol use, etc.)

EMR text:
{emr_text}"""

    # Generate text completion
    completion_text = generate_text_completion(prompt, "text-davinci-002", api_key)
    # print(completion_text)

    # Initialize entity values
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
    text = completion_text["choices"][0]["text"]
    print(text)

    # Extract entities from completion text
    if completion_text["choices"][0]["text"] is not None:


        lines = completion_text["choices"][0]["text"].split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("Patient's age:"):
                entities["age"] = line.split(":", 1)[1].strip()
            elif line.startswith("Patient's gender:"):
                entities["gender"] = line.split(":", 1)[1].strip()
            elif line.startswith("Patient's diagnoses:"):
                diagnoses = line.split(":", 1)[1].strip()
                entities["diagnoses"] = re.split(r",\s*", diagnoses)
            elif line.startswith("Patient's medications:"):
                medications = line.split(":", 1)[1].strip()
                entities["medications"] = re.split(r",\s*", medications)
            elif line.startswith("Patient's allergies:"):
                allergies = line.split(":", 1)[1].strip()
                entities["allergies"] = re.split(r",\s*", allergies)
            elif line.startswith("Patient's vital signs:"):
                vital_signs = line.split(":", 1)[1].strip()
                entities["vital_signs"] = re.split(r",\s*", vital_signs)
            elif line.startswith("Patient's test results:"):
                test_results = line.split(":", 1)[1].strip()
                entities["test_results"] = re.split(r",\s*", test_results)
            elif line.startswith("Patient's past medical history:"):
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


emr_text = '''Patient is a 25 year old female with a diagnosis of asthma. She is currently taking Albuterol and Fluticasone inhalers for her symptoms. 
She has no known allergies. Her vital signs today include a blood pressure of 120/80 mmHg and a heart rate of 70 bpm. 
She has recently had a chest x-ray, the results of which were normal. She has a history of eczema and her mother has a history of hypertension.
 The patient does not smoke or drink alcohol.'''
