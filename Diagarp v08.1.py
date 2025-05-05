import streamlit as st
import json
import os

# --- Localization & Media Support ---
def load_translations():
    return {
        'en': {},
        'ha': {
            'Select Language': 'Zaɓi Harshe',
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

# --- App Configuration ---
EMERGENCY_VET_CONTACT = {
    'Nigeria': '+234XXXXXXXXXX',
    'Kenya': '+254XXXXXXXXX',
    'Uganda': '+256XXXXXXXXX',
    'Other': 'N/A'
}
LOG_FILE = 'symptom_logs.json'

# Ensure log file exists
def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)

# Log user responses
def log_symptoms(key, responses):
    with open(LOG_FILE, 'r+') as f:
        data = json.load(f)
        data.append({'disease': key, 'responses': responses})
        f.seek(0);
        json.dump(data, f, indent=2)

# --- Disease Data ---
DISEASES = [
    # definitions with 'criteria', 'images', 'summary' as before...
]
SYMPTOM_MAP = {
    'Drooling & blisters': 'fmd',
    'Deep cough & labored breathing': 'cbpp',
    'Weight loss & anemia': 'trypanosomiasis',
    'Skin nodules': 'lsd',
    'Red or dark urine': 'babesiosis',
    'Anemia without red urine': 'anaplasmosis',
    'Swollen lymph nodes & dyspnea': 'ecf',
    'Late-term abortion': 'brucellosis',
    'Sudden death in young cattle': 'blackleg',
    'Chronic diarrhea & weight loss': 'parasites'
}

# --- State Management ---
def init_state():
    if 'stage' not in st.session_state:
        st.session_state.stage = 'lang'
        st.session_state.responses = []
        st.session_state.index = 0
        st.session_state.lang = 'en'
        st.session_state.selected = None

# --- UI Components ---
def sidebar_setup():
    logo_path = 'images/logo.png'
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
    st.sidebar.markdown('## ' + t('Cattle Disease Diagnostic'))
    st.sidebar.selectbox(t('Select Language'), ['en', 'ha'], key='lang')
    st.sidebar.selectbox('Region', list(EMERGENCY_VET_CONTACT.keys()), key='region')
    st.sidebar.markdown('---')
    progress = 0
    if st.session_state.stage == 'symptom':
        progress = 1
    elif st.session_state.stage == 'question':
        disease = st.session_state.selected
        total = len(disease['criteria'])
        progress = 1 + (st.session_state.index / total)
    elif st.session_state.stage == 'result':
        progress = 1
    st.sidebar.progress(progress)(progress)

# --- Pages ---
def page_symptom():
    st.header(t('What is the primary symptom observed?'))
    symptom = st.radio('', list(SYMPTOM_MAP.keys()), horizontal=True)
    if st.button(t('Next')):
        code = SYMPTOM_MAP[symptom]
        st.session_state.selected = next(d for d in DISEASES if d['key'] == code)
        st.session_state.stage = 'question'


def page_question():
    disease = st.session_state.selected
    crit = disease['criteria'][st.session_state.index]
    st.subheader(f"{t('Question')} {st.session_state.index+1} {t('of')} {len(disease['criteria'])}")
    img_path = disease['images'][st.session_state.index % len(disease['images'])]
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    ans = st.radio(t(crit['question']), crit['options'])
    cols = st.columns(3)
    if cols[1].button(t('Next')):(t('Next')):
        st.session_state.responses.append((crit, ans))
        st.session_state.index += 1
        if st.session_state.index >= len(disease['criteria']):
            st.session_state.stage = 'result'


def page_result():
    disease = st.session_state.selected
    positive = all(ans in crit['positive'] for crit, ans in st.session_state.responses)
    if positive:
        st.success(f"✅ {t('Likely diagnosis:')} {disease['name']}")
    else:
        st.error(f"❌ {t('Symptoms do not fully match. Please consult a veterinarian.')} ")
    st.write(t(disease['summary']))
    st.markdown(f"**Emergency vet:** {EMERGENCY_VET_CONTACT[st.session_state.region]}")
    if st.button(t('Restart')):
        for k in ['stage','responses','index','selected']: st.session_state.pop(k, None)
        st.session_state.stage = 'symptom'

# --- Main ---
def main():
    init_log()
    init_state()
    sidebar_setup()

    if st.session_state.stage == 'lang':
        st.session_state.stage = 'symptom'
    if st.session_state.stage == 'symptom':
        page_symptom()
    elif st.session_state.stage == 'question':
        page_question()
    else:
        page_result()

if __name__ == '__main__':
    main()
