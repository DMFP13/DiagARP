import streamlit as st
import json
import os

# --- Localization & Media Support ---

def load_translations():
    return {
        'en': {},
        'ha': {
            'Next': 'Gaba',
            'Cattle Disease Diagnostic': 'Gwajin Cutar Shanu',
            'What is the primary symptom observed?': 'Menene babban alamar da aka gani?',
            'Question': 'Tambaya',
            'of': 'na',
            'Likely diagnosis:': 'Hasashen cuta:',
            'Symptoms do not fully match. Please consult a veterinarian.': 'Alamomin ba su dace sosai ba. Da fatan za a tuntubi likitan dabbobi.',
            'Restart': 'Fara Sake',
        }
    }

def t(text: str) -> str:
    lang = st.session_state.get('lang', 'en')
    return load_translations().get(lang, {}).get(text, text)

# --- Configuration ---
EMERGENCY_VET_CONTACT = {
    'Nigeria': '+234XXXXXXXXXX',
    'Kenya': '+254XXXXXXXXX',
    'Uganda': '+256XXXXXXXXX',
    'Other': 'N/A'
}
LOG_FILE = 'symptom_logs.json'

# --- Disease Data ---
DISEASES = [
    {
        'key': 'fmd',
        'name': 'Foot-and-Mouth Disease',
        'summary': 'Viral disease marked by fever, drooling, and blisters in the mouth and on the feet.',
        'images': ['images/fmd_mouth.jpg', 'images/fmd_foot.jpg'],
        'criteria': [
            {'question': 'Is the cow drooling or foaming at the mouth?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Do you see blisters or raw ulcers in the cow’s mouth?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is the cow lame or reluctant to move due to hoof lesions?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Have multiple animals shown these signs at the same time?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Was there recent movement of animals into the herd?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    # ... other diseases defined similarly ...
]
SYMPTOM_MAP = {
    'Drooling & blisters': 'fmd',
    # ... map other symptoms ...
}

# --- Logging ---
def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)

def log_symptoms(disease_key, responses):
    try:
        with open(LOG_FILE, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append({'disease': disease_key, 'responses': responses})
            f.seek(0)
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Logging error: {e}")

# --- State Management ---
def init_state():
    if 'stage' not in st.session_state:
        st.session_state.stage = 'symptom'
        st.session_state.selected = None
        st.session_state.responses = []
        st.session_state.index = 0
        # default language and region
        st.session_state.lang = 'en'
        st.session_state.region = 'Nigeria'

# --- UI Components ---
def sidebar_setup():
    logo = 'images/logo.png'
    if os.path.exists(logo):
        try:
            st.sidebar.image(logo, use_container_width=True)
        except:
            pass
    st.sidebar.title(t('Cattle Disease Diagnostic'))
    st.sidebar.selectbox('Region', list(EMERGENCY_VET_CONTACT.keys()), key='region')
    st.sidebar.markdown('---')
    # Progress: 0-100
    if st.session_state.stage == 'symptom':
        p = 0
    elif st.session_state.stage == 'question':
        total = len(st.session_state.selected['criteria'])
        p = int(((st.session_state.index + 1)/total)*100)
    else:
        p = 100
    st.sidebar.progress(p)

# --- Pages ---
def page_symptom():
    st.header(t('What is the primary symptom observed?'))
    form = st.form(key='symptom_form')
    choice = form.radio('', list(SYMPTOM_MAP.keys()), horizontal=True)
    if form.form_submit_button(t('Next')):
        key = SYMPTOM_MAP[choice]
        st.session_state.selected = next(d for d in DISEASES if d['key']==key)
        st.session_state.stage = 'question'
        st.session_state.responses = []
        st.session_state.index = 0


def page_question():
    disease = st.session_state.selected
    idx = st.session_state.index
    crit = disease['criteria'][idx]
    st.subheader(f"{t('Question')} {idx+1} {t('of')} {len(disease['criteria'])}")
    img_path = disease['images'][idx % len(disease['images'])]
    if os.path.exists(img_path):
        try:
            st.image(img_path, use_container_width=True)
        except:
            pass
    form = st.form(key=f'question_form_{idx}')
    ans = form.radio(t(crit['question']), crit['options'])
    if form.form_submit_button(t('Next')):
        st.session_state.responses.append({'question': crit['question'], 'answer': ans})
        if ans not in crit['positive']:
            st.session_state.stage = 'result'
        else:
            st.session_state.index += 1
            if st.session_state.index >= len(disease['criteria']):
                st.session_state.stage = 'result'


def page_result():
    disease = st.session_state.selected
    match = (st.session_state.stage == 'result') and all(
        r['answer'] in next(c for c in disease['criteria'] if c['question']==r['question'])['positive']
        for r in st.session_state.responses
    )
    log_symptoms(disease['key'] if match else 'none', st.session_state.responses)
    if match:
        st.success(f"✅ {t('Likely diagnosis:')} {disease['name']}")
        st.write(disease['summary'])
    else:
        st.error(t('Symptoms do not fully match. Please consult a veterinarian.'))
    st.markdown(f"**Emergency vet:** {EMERGENCY_VET_CONTACT[st.session_state.region]}")
    if st.button(t('Restart')):
        for k in list(st.session_state.keys()):
            if k not in ['lang', 'region']:
                del st.session_state[k]
        init_state()

# --- Main ---
def main():
    init_log()
    init_state()
    sidebar_setup()
    if st.session_state.stage == 'symptom':
        page_symptom()
    elif st.session_state.stage == 'question':
        page_question()
    else:
        page_result()

if __name__ == '__main__':
    main()
