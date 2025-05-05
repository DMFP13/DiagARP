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
        f.seek(0)
        json.dump(data, f, indent=2)

# --- Disease Data ---
DISEASES = [ ... ]  # unchanged disease list
SYMPTOM_MAP = { ... }  # unchanged symptom map

# --- State Management ---
def init_state():
    if 'stage' not in st.session_state:
        st.session_state.update({
            'stage': 'lang',
            'responses': [],
            'index': 0,
            'lang': 'en',
            'selected': None
        })

# --- UI Components ---
def sidebar_setup():
    logo = 'images/logo.png'
    if os.path.exists(logo):
        st.sidebar.image(logo, use_container_width=True)
    st.sidebar.markdown('## ' + t('Cattle Disease Diagnostic'))
    st.sidebar.selectbox(t('Select Language'), ['en','ha'], key='lang')
    st.sidebar.selectbox('Region', list(EMERGENCY_VET_CONTACT.keys()), key='region')
    st.sidebar.markdown('---')
    # 0-100 progress
    if st.session_state.stage == 'symptom':
        p = 0
    elif st.session_state.stage == 'question':
        total = len(st.session_state.selected['criteria'])
        p = int((st.session_state.index/total)*100)
    else:
        p = 100
    st.sidebar.progress(p)

# --- Pages ---
def page_symptom():
    st.header(t('What is the primary symptom observed?'))
    choice = st.radio('', list(SYMPTOM_MAP.keys()), horizontal=True)
    if st.button(t('Next')):
        disease_key = SYMPTOM_MAP[choice]
        st.session_state.selected = next(d for d in DISEASES if d['key']==disease_key)
        st.session_state.stage = 'question'


def page_question():
    disease = st.session_state.selected
    idx = st.session_state.index
    crit = disease['criteria'][idx]
    st.subheader(f"{t('Question')} {idx+1} {t('of')} {len(disease['criteria'])}")
    img = disease['images'][idx % len(disease['images'])]
    if os.path.exists(img): st.image(img, use_container_width=True)
    ans = st.radio(t(crit['question']), crit['options'])
    if st.button(t('Next')):
        st.session_state.responses.append((crit, ans))
        # Early exit on negative
        if ans not in crit['positive']:
            st.session_state.stage = 'result'
        else:
            st.session_state.index += 1
            if st.session_state.index >= len(disease['criteria']):
                st.session_state.stage = 'result'


def page_result():
    disease = st.session_state.selected
    # Log
    log_symptoms(disease['key'], st.session_state.responses)
    # Determine outcome
    match = all(ans in crit['positive'] for crit, ans in st.session_state.responses)
    if match:
        st.success(f"✅ {t('Likely diagnosis:')} {disease['name']}")
        st.write(t(disease['summary']))
    else:
        st.error(f"❌ {t('Symptoms do not fully match. Please consult a veterinarian.')}")
    st.markdown(f"**Emergency vet:** {EMERGENCY_VET_CONTACT[st.session_state.region]}")
    if st.button(t('Restart')):
        for k in ['stage','responses','index','selected']: st.session_state.pop(k,None)
        st.session_state.stage='symptom'

# --- Main ---
def main():
    init_log(); init_state(); sidebar_setup()
    if st.session_state.stage=='lang': st.session_state.stage='symptom'
    if st.session_state.stage=='symptom': page_symptom()
    elif st.session_state.stage=='question': page_question()
    else: page_result()

if __name__=='__main__': main()
