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
    # ... include other diseases similarly ...
]

# Wizard state management
def init_state():
    if 'stage' not in st.session_state:
        st.session_state.stage = 'select'  # stages: select, question, result
        st.session_state.selected_disease = None
        st.session_state.responses = []
        st.session_state.q_index = 0

# Run one question
def run_question():
    disease = st.session_state.selected_disease
    criteria = disease['criteria']
    idx = st.session_state.q_index
    crit = criteria[idx]
    st.write(f"**Question {idx+1} of {len(criteria)}**")
    ans = st.radio(crit['question'], crit['options'], key=f"q{idx}")
    if st.button('Next'):
        st.session_state.responses.append((crit['question'], ans))
        st.session_state.q_index += 1
        if st.session_state.q_index >= len(criteria):
            st.session_state.stage = 'result'
        st.experimental_rerun()

# Show result
def show_result():
    disease = st.session_state.selected_disease
    # Evaluate
    positive = all(ans in crit['positive'] for (crit, (_, ans)) in zip(disease['criteria'], [(q,a) for q,a in st.session_state.responses]))
    if positive:
        st.success(f"Likely diagnosis: {disease['name']}")
        st.write(disease['summary'])
    else:
        st.error("Symptoms do not fully match. Please consult a veterinarian.")
    st.info(f"Emergency vet contact: {EMERGENCY_VET_CONTACT[st.session_state.region]}")
    if st.button('Start Over'):
        for k in ['stage','selected_disease','responses','q_index']:
            del st.session_state[k]
        st.experimental_rerun()

# Main app
def main():
    st.title('Cattle Disease Diagnostic')
    init_log()
    init_state()

    if st.session_state.stage == 'select':
        st.session_state.region = st.selectbox('Select Region', list(EMERGENCY_VET_CONTACT.keys()))
        disease_names = [d['name'] for d in DISEASES]
        choice = st.selectbox('Select Disease to Diagnose', [''] + disease_names)
        if choice and st.button('Start Diagnosis'):
            st.session_state.selected_disease = next(d for d in DISEASES if d['name']==choice)
            st.session_state.stage = 'question'
            st.experimental_rerun()

    elif st.session_state.stage == 'question':
        run_question()

    elif st.session_state.stage == 'result':
        show_result()

if __name__ == '__main__':
    main()
V