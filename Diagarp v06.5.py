import streamlit as st
import json
import os

# --- Configuration & Data Definitions ---
# Stub for localized language support
def load_translations():
    return {
        'en': {},  # English (default)
        # Add other languages here
    }

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
diSEASES = [
    {
        'key': 'fmd',
        'name': 'Foot-and-Mouth Disease',
        'summary': 'Viral; fever, drooling, blisters in mouth & on feet.',
        'images': ['images/fmd_mouth.jpg', 'images/fmd_foot.jpg'],
        'criteria': [
            {'question': 'Is the cow drooling excessively or foaming at the mouth?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you see blisters or raw ulcers in the mouth?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow lame or reluctant to move due to hoof lesions?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have multiple animals shown these signs at once?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Was there recent introduction of new animals?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'cbpp',
        'name': 'Contagious Bovine Pleuropneumonia',
        'summary': 'Bacterial; painful cough, labored breathing.',
        'images': ['images/cbpp_cough.jpg', 'images/cbpp_pleura.jpg'],
        'criteria': [
            {'question': 'Is there a deep, painful cough?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is breathing labored or painful?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Does the cow grunt on exhalation when breathing?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there a thick or blood-stained nasal discharge?', 'options': ['Thick', 'Clear', 'None'], 'positive': ['Thick']},
            {'question': 'Has illness lasted weeks and affected others?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the herd unvaccinated in an endemic area?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'trypanosomiasis',
        'name': 'Trypanosomiasis (Nagana)',
        'summary': 'Parasitic; intermittent fever, anemia, weight loss.',
        'images': ['images/nagana_anemia.jpg', 'images/tsetse_fly.jpg'],
        'criteria': [
            {'question': 'Has the cow lost weight steadily over weeks?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are the eyes or gums pale or white?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Has the cow had on-and-off fever episodes?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or lethargic?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you palpate swollen lymph nodes or bottle jaw?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is this a tsetse fly–infested area?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'lsd',
        'name': 'Lumpy Skin Disease',
        'summary': 'Viral; firm skin nodules, fever, lymph node enlargement.',
        'images': ['images/lsd_nodules.jpg', 'images/lsd_lymph.jpg'],
        'criteria': [
            {'question': 'Does the cow have multiple firm skin nodules?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Did fever precede the nodules?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are nodules painful, ~2–5 cm diameter?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have other cattle developed similar nodules?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there tearing of eyes or nasal discharge?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Were new cattle introduced recently?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'babesiosis',
        'name': 'Babesiosis (Redwater)',
        'summary': 'Tick-borne; red urine, high fever, anemia.',
        'images': ['images/babesiosis_urine.jpg', 'images/blue_tick.jpg'],
        'criteria': [
            {'question': 'Have you seen red or dark-colored urine?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Does the cow have a high fever (40–42°C)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are eyes or gums pale or yellow?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or isolating from the herd?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are ticks present on the animal?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is this an adult or newly introduced cow?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'anaplasmosis',
        'name': 'Anaplasmosis',
        'summary': 'Tick-borne; anemia, fever, no red urine.',
        'images': ['images/anaplasmosis_jaundice.jpg'],
        'criteria': [
            {'question': 'Is the cow febrile (~41°C)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is urine normal color (no hemoglobinuria)?', 'options': ['Normal', 'Red'], 'positive': ['Normal']},
            {'question': 'Are mucous membranes pale or jaundiced?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or breathless on movement?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is this an adult animal?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are ticks present or area endemic?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'ecf',
        'name': 'East Coast Fever',
        'summary': 'Theileria; swollen lymph nodes, high fever, respiratory distress.',
        'images': ['images/ecf_nodes.jpg'],
        'criteria': [
            {'question': 'Are you in an ECF-endemic region?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are superficial lymph nodes visibly swollen?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there a very high fever (>41°C)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Has the cow developed respiratory distress?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there tearing of eyes or nasal discharge?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are brown ear ticks present?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'brucellosis',
        'name': 'Brucellosis',
        'summary': 'Bacterial; late-term abortion, retained placenta.',
        'images': ['images/brucellosis_abortion.jpg'],
        'criteria': [
            {'question': 'Has the cow aborted in late pregnancy?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Did placenta remain attached after birth?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have multiple cows aborted recently?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you see joint swellings (hygromas)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have bulls shown swollen testicles?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Any undulating fevers in farm workers?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'blackleg',
        'name': 'Blackleg',
        'summary': 'Clostridial; sudden death in young cattle, gas gangrene.',
        'images': ['images/blackleg_swelling.jpg'],
        'criteria': [
            {'question': 'Was a young animal found dead suddenly?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Was there a hot swelling in a muscle or limb?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Could you feel gas crackling under the skin?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'If observed alive, was the animal febrile and depressed?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have similar deaths occurred in other young cattle?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'parasites',
        'name': 'Parasitic Gastroenteritis',
        'summary': 'Helminthiasis; poor condition, diarrhea, anemia.',
        'images': ['images/bottle_jaw.jpg'],
        'criteria': [
            {'question': 'Are young cattle losing weight despite good feed?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there chronic diarrhea or loose stools?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you see pale membranes or bottle jaw?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are calves and yearlings more affected?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is pasture wet or deworming infrequent?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do any cattle cough (lungworm)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    }
]

# Streamlit UI Functions

def check_disease(disease):
    st.header(disease['name'])
    responses = {}
    match = True
    for crit in disease['criteria']:
        ans = st.radio(crit['question'], crit['options'], key=disease['key'] + crit['question'])
        responses[crit['question']] = ans
        if ans not in crit['positive']:
            match = False
    log_symptoms(disease['key'], responses)
    return match

# Main App
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
                    for img in d['images']:
                        st.image(img, use_column_width=True)
                    st.info(f"Emergency vet contact: {EMERGENCY_VET_CONTACT[region]}")
                    found = True
                    break
        if not found:
            st.error('No matching diagnosis found. Please consult a vet.')

if __name__ == '__main__':
    main()
