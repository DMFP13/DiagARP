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
    {
        'key': 'cbpp',
        'name': 'Contagious Bovine Pleuropneumonia',
        'summary': 'Bacterial lung infection causing deep cough, painful breathing, and nasal discharge.',
        'images': ['images/cbpp_cough.jpg','images/cbpp_pleura.jpg'],
        'criteria': [
            {'question': 'Is the cow coughing deeply and painfully?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Does the cow grunt or show labored breathing?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is there thick or blood-stained nasal discharge?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Has the illness persisted for weeks and affected other cattle?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is the herd unvaccinated in an endemic area?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'trypanosomiasis',
        'name': 'Trypanosomiasis (Nagana)',
        'summary': 'Parasitic disease with intermittent fever, anemia, weight loss, and weakness.',
        'images': ['images/nagana_anemia.jpg','images/tsetse_fly.jpg'],
        'criteria': [
            {'question': 'Has the cow lost weight over several weeks?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Are the eyes or gums pale (anemia)?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Has the fever been intermittent (on and off)?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or lethargic?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Are lymph nodes swollen or is there bottle jaw?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'lsd',
        'name': 'Lumpy Skin Disease',
        'summary': 'Viral illness with firm, raised skin nodules, fever, and lymph node enlargement.',
        'images': ['images/lsd_nodules.jpg','images/lsd_lymph.jpg'],
        'criteria': [
            {'question': 'Does the cow have multiple firm skin nodules?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Did fever occur before or during nodule appearance?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Have other cattle developed similar nodules?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is there eye tearing or nasal discharge?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Were new animals introduced from an infected area?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'babesiosis',
        'name': 'Babesiosis (Redwater)',
        'summary': 'Tick-borne; high fever, anemia, and red or dark-colored urine.',
        'images': ['images/babesiosis_urine.jpg','images/blue_tick.jpg'],
        'criteria': [
            {'question': 'Have you seen red or dark-colored urine?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Does the cow have a high fever (40–42°C)?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Are the eyes or gums pale or yellowish?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or isolating from the herd?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Are ticks visible on the cow?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'anaplasmosis',
        'name': 'Anaplasmosis',
        'summary': 'Tick-borne bacterial disease causing fever, severe anemia, and no red urine.',
        'images': ['images/anaplasmosis_jaundice.jpg'],
        'criteria': [
            {'question': 'Is the cow feverish (around 41°C)?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is the urine normal color (no hemoglobinuria)?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Are the mucous membranes pale or jaundiced?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or breathless on exertion?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'ecf',
        'name': 'East Coast Fever',
        'summary': 'Protozoal disease with high fever, marked lymph node swelling, and respiratory distress.',
        'images': ['images/ecf_nodes.jpg'],
        'criteria': [
            {'question': 'Are superficial lymph nodes visibly swollen?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is the fever very high (>41°C)?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Does the cow have difficulty breathing?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is there nasal discharge or tearing of eyes?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'brucellosis',
        'name': 'Brucellosis',
        'summary': 'Bacterial reproductive disease causing late-term abortion and retained placenta.',
        'images': ['images/brucellosis_abortion.jpg'],
        'criteria': [
            {'question': 'Has the cow recently aborted late in pregnancy?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Did the placenta remain attached after birth?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Have multiple cows aborted in the herd?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Do you notice joint swellings (hygromas)?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'blackleg',
        'name': 'Blackleg',
        'summary': 'Clostridial infection causing sudden death and muscle swelling in young cattle.',
        'images': ['images/blackleg_swelling.jpg'],
        'criteria': [
            {'question': 'Was a young animal found dead suddenly?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Was there rapid muscle swelling before death?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Could you feel crackling gas under the skin?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'If observed alive, was the animal feverish and depressed?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    },
    {
        'key': 'parasites',
        'name': 'Parasitic Gastroenteritis',
        'summary': 'Helminth infestation causing poor condition, diarrhea, anemia, and bottle jaw.',
        'images': ['images/bottle_jaw.jpg'],
        'criteria': [
            {'question': 'Are young cattle losing condition despite good feed?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Is there chronic diarrhea in the herd?', 'options': ['Yes','No'], 'positive': ['Yes']},
            {'question': 'Do you see pale membranes or fluid under the jaw?', 'options': ['Yes','No'], 'positive': ['Yes']}
        ]
    }
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
    st.sidebar.progress(progress)

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
    if cols[1].button(t('Next')):
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
        st.error(f"❌ {t('Symptoms do not fully match. Please consult a veterinarian.')}")
    st.write(t(disease['summary']))
    st.markdown(f"**Emergency vet:** {EMERGENCY_VET_CONTACT[st.session_state.region]}")
    if st.button(t('Restart')):
        for k in ['stage', 'responses', 'index', 'selected']:
            st.session_state.pop(k, None)
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
