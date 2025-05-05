import streamlit as st
import json
import os

# --- App Data ---
LOG_FILE = 'symptom_logs.json'
EMERGENCY_VET_CONTACT = {
    'Nigeria': '+234XXXXXXXXXX',
    'Kenya': '+254XXXXXXXXX',
    'Uganda': '+256XXXXXXXXX',
    'Other': 'N/A'
}

DISEASES = [
    {
        'key': 'fmd',
        'name': 'Foot-and-Mouth Disease',
        'summary': 'Viral disease marked by fever, drooling, and blisters in the mouth and on the feet.',
        'criteria': [
            {'question': 'Is the cow drooling or foaming at the mouth?', 'positive': ['Yes']},
            {'question': 'Do you see blisters or raw ulcers in the cow’s mouth?', 'positive': ['Yes']},
            {'question': 'Is the cow lame or reluctant to move due to hoof lesions?', 'positive': ['Yes']},
            {'question': 'Have multiple animals shown these signs at the same time?', 'positive': ['Yes']},
            {'question': 'Was there recent movement of animals into the herd?', 'positive': ['Yes']}
        ]
    },
    {
        'key': 'cbpp',
        'name': 'Contagious Bovine Pleuropneumonia',
        'summary': 'Bacterial lung infection causing deep cough, painful breathing, and nasal discharge.',
        'criteria': [
            {'question': 'Is the cow coughing deeply and painfully?', 'positive': ['Yes']},
            {'question': 'Does the cow grunt or show labored breathing?', 'positive': ['Yes']},
            {'question': 'Is there thick or blood-stained nasal discharge?', 'positive': ['Yes']},
            {'question': 'Has the illness persisted for weeks and affected other cattle?', 'positive': ['Yes']},
            {'question': 'Is the herd unvaccinated in an endemic area?', 'positive': ['Yes']}
        ]
    },
    # ... include other diseases similarly ...
]

# Ensure log exists
def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)

# Log responses
def log_symptoms(disease_key, responses):
    with open(LOG_FILE, 'r+') as f:
        data = json.load(f)
        data.append({'disease': disease_key, 'responses': responses})
        f.seek(0)
        json.dump(data, f, indent=2)

# Initialize session state
def init_state():
    if 'd_idx' not in st.session_state:
        st.session_state.update({
            'd_idx': 0,
            'q_idx': 0,
            'responses': [],
            'matched': None
        })

# Display one question per page

def page_question():
    d = DISEASES[st.session_state.d_idx]
    crit = d['criteria'][st.session_state.q_idx]
    st.header(f"{d['name']} — Question {st.session_state.q_idx+1} of {len(d['criteria'])}")
    ans = st.radio(crit['question'], ['Yes', 'No'])
    if st.button('Next'):
        st.session_state.responses.append({'question': crit['question'], 'answer': ans})
        # If answer not positive, try next disease
        if ans not in crit['positive']:
            st.session_state.d_idx += 1
            st.session_state.q_idx = 0
            # If no more diseases, go to result
            if st.session_state.d_idx >= len(DISEASES):
                st.session_state.matched = None
                st.session_state.stage = 'result'
                return
        else:
            st.session_state.q_idx += 1
            # If criteria exhausted, disease matched
            if st.session_state.q_idx >= len(d['criteria']):
                st.session_state.matched = d
                st.session_state.stage = 'result'
                return

# Show result

def page_result():
    if st.session_state.matched:
        d = st.session_state.matched
        st.success(f"Likely diagnosis: {d['name']}")
        st.write(d['summary'])
        log_symptoms(d['key'], st.session_state.responses)
    else:
        st.error("No matching diagnosis found. Please consult a veterinarian.")
        log_symptoms('none', st.session_state.responses)
    st.info(f"Emergency vet contact: {EMERGENCY_VET_CONTACT.get('Nigeria')}")
    if st.button('Restart'):
        for k in ['d_idx','q_idx','responses','matched','stage']:
            st.session_state.pop(k, None)
        init_state()
        st.experimental_rerun()

# Main app

def main():
    init_log()
    init_state()
    # Default stage
    if 'stage' not in st.session_state:
        st.session_state.stage = 'question'

    if st.session_state.stage == 'question':
        page_question()
    else:
        page_result()

if __name__ == '__main__':
    main()
