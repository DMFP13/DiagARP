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
    }
]

# Map primary symptom to disease key
SYMPTOM_MAP = {
    'Drooling & blisters': 'fmd',
    'Deep cough & labored breathing': 'cbpp',
    'Weight loss & anemia': 'trypanosomiasis',
    'Skin nodules': 'lsd'
}

# Wizard state management

def init_state():
    if 'stage' not in st.session_state:
        st.session_state.stage = 'symptom'  # symptom, question, result
        st.session_state.selected = None
        st.session_state.responses = []
        st.session_state.index = 0

# Display symptom selection

def select_symptom():
    st.title('Cattle Disease Diagnostic')
    symptom = st.radio(
        'What is the primary symptom observed?',
        list(SYMPTOM_MAP.keys())
    )
    if st.button('Next'):
        key = SYMPTOM_MAP[symptom]
        st.session_state.selected = next(d for d in DISEASES if d['key'] == key)
        st.session_state.stage = 'question'

# Display one question per page

def run_question():
    disease = st.session_state.selected
    crit = disease['criteria'][st.session_state.index]
    st.write(f"**Question {st.session_state.index+1} of {len(disease['criteria'])}**")
    ans = st.radio(crit['question'], crit['options'], key=f"q{st.session_state.index}")
    if st.button('Next'):
        st.session_state.responses.append((crit, ans))
        st.session_state.index += 1
        if st.session_state.index >= len(disease['criteria']):
            st.session_state.stage = 'result'

# Show final diagnosis

def show_result():
    disease = st.session_state.selected
    positive = all(ans in crit['positive'] for (crit, ans) in st.session_state.responses)
    if positive:
        st.success(f"Likely diagnosis: {disease['name']}")
        st.write(disease['summary'])
    else:
        st.error("Symptoms do not fully match. Please consult a veterinarian.")
    st.info(f"Emergency vet contact: {EMERGENCY_VET_CONTACT['Nigeria']}")
    if st.button('Restart'):
        for key in ['stage', 'selected', 'responses', 'index']:
            st.session_state.pop(key, None)

# Main application

def main():
    init_log()
    init_state()

    if st.session_state.stage == 'symptom':
        select_symptom()
    elif st.session_state.stage == 'question':
        run_question()
    elif st.session_state.stage == 'result':
        show_result()

if __name__ == '__main__':
    main()
