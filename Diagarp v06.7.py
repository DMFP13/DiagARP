import streamlit as st
import json
import os

# --- Configuration & Data Definitions ---
# Stub for localized language support
def load_translations():
    return {'en': {}}

# Emergency contacts per region
EMERGENCY_VET_CONTACT = {
    'Nigeria': '+234XXXXXXXXXX',
    'Kenya': '+254XXXXXXXXX',
    'Uganda': '+256XXXXXXXXX',
    'Other': 'N/A'
}

# Log file for symptom responses
LOG_FILE = 'symptom_logs.json'

# Ensure log file exists
def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)

# Append a new log entry
def log_symptoms(disease_key, responses):
    with open(LOG_FILE, 'r+') as f:
        data = json.load(f)
        data.append({'disease': disease_key, 'responses': responses})
        f.seek(0)
        json.dump(data, f, indent=2)

# Disease definitions
DISEASES = [
    {
        'key': 'fmd',
        'name': 'Foot-and-Mouth Disease',
        'summary': 'Viral disease marked by fever, drooling, and blisters in the mouth and on the feet.',
        'criteria': [
            {'question': 'Is the cow drooling or foaming at the mouth?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you see blisters or raw ulcers in the cow’s mouth?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow lame or reluctant to move due to hoof lesions?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have multiple animals shown these signs at the same time?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Was there recent movement of animals into the herd?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'cbpp',
        'name': 'Contagious Bovine Pleuropneumonia',
        'summary': 'Bacterial lung infection causing deep cough and labored breathing.',
        'criteria': [
            {'question': 'Is the cow coughing deeply and painfully?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Does the cow have difficulty breathing or grunt on exhale?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there thick or blood-stained nasal discharge?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Has the illness persisted for weeks and affected other cattle?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the herd unvaccinated in a region known for this disease?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'trypanosomiasis',
        'name': 'Trypanosomiasis (Nagana)',
        'summary': 'Parasitic disease with intermittent fever, anemia, and weight loss.',
        'criteria': [
            {'question': 'Has the cow lost weight over several weeks?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are the eyes or gums pale (anemia)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Has the fever been intermittent (on and off)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak, lethargic, or isolated from the herd?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are lymph nodes swollen or is there bottle jaw?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'lsd',
        'name': 'Lumpy Skin Disease',
        'summary': 'Viral illness with firm, raised skin nodules and fever.',
        'criteria': [
            {'question': 'Does the cow have multiple firm skin nodules?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Did fever occur before or during nodule appearance?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have other cattle developed similar nodules?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there eye tearing or nasal discharge?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Were new animals introduced from elsewhere?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'babesiosis',
        'name': 'Babesiosis (Redwater)',
        'summary': 'Tick-borne parasite causing high fever and red or dark urine.',
        'criteria': [
            {'question': 'Have you seen red or brown urine?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Does the cow have a high fever (around 40°C)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are the eyes or gums pale or yellowish?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or separating from the herd?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are ticks visible on the cow?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'anaplasmosis',
        'name': 'Anaplasmosis',
        'summary': 'Tick-borne bacterial disease causing anemia and fever, no red urine.',
        'criteria': [
            {'question': 'Is the cow feverish (around 41°C)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is urine normal color (no hemoglobinuria)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are mucous membranes pale or yellow?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or breathless on movement?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'ecf',
        'name': 'East Coast Fever',
        'summary': 'Theileria parasite with swollen lymph nodes and respiratory distress.',
        'criteria': [
            {'question': 'Are superficial lymph nodes visibly swollen?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Does the cow have a very high fever (>41°C)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow experiencing difficulty breathing?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there eye tearing or nasal discharge?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'brucellosis',
        'name': 'Brucellosis',
        'summary': 'Bacterial infection causing late-term abortion and retained placenta.',
        'criteria': [
            {'question': 'Has the cow recently aborted in late pregnancy?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Did the placenta remain attached after birth?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have multiple cows aborted in the herd?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you notice joint swellings (hygromas)?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'blackleg',
        'name': 'Blackleg',
        'summary': 'Clostridial disease causing sudden death and muscle swelling in young cattle.',
        'criteria': [
            {'question': 'Was a young animal found dead suddenly?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Was there rapid muscle swelling before death?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Could you feel crackling gas under the skin?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'If observed alive, was the animal feverish and depressed?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'parasites',
        'name': 'Parasitic Gastroenteritis',
        'summary': 'Worm burden causing poor condition, diarrhea, and anemia.',
        'criteria': [
            {'question': 'Are young cattle losing condition despite good feed?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there chronic diarrhea in the herd?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you see pale membranes or fluid under the jaw?', 'options': ['Yes', 'No'], 'positive': ['Yes']}
        ]
    }
]

# Streamlit UI

def check_disease(d):
    st.subheader(d['name'])
    responses = {}
    match = True
    for crit in d['criteria']:
        ans = st.radio(crit['question'], crit['options'], key=d['key'] + crit['question'])
        responses[crit['question']] = ans
        if ans not in crit['positive']:
            match = False
    log_symptoms(d['key'], responses)
    return match

# Main Application

def main():
    st.title('Cattle Disease Diagnostic')
    init_log()

    region = st.selectbox('Select Region', list(EMERGENCY_VET_CONTACT.keys()))
    diseases_to_check = st.multiselect('Choose diseases (leave blank to check all)', [d['name'] for d in DISEASES])

    if st.button('Run Diagnosis'):
        found = False
        for d in DISEASES:
            if not diseases_to_check or d['name'] in diseases_to_check:
                if check_disease(d):
                    st.success(f"Likely diagnosis: {d['name']}")
                    st.write(d['summary'])
                    st.info(f"Emergency vet contact: {EMERGENCY_VET_CONTACT[region]}")
                    found = True
                    break
        if not found:
            st.error('No matching diagnosis found. Please consult a veterinarian.')

if __name__ == '__main__':
    main()
