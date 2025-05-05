```python
import streamlit as st
import json
import os

# --- Configuration & Data Definitions ---
# Stub for localized language support
def load_translations():
    return {
        'en': {},  # English (default)
        # Add other languages (e.g., 'ha': Hausa, 'yo': Yoruba)
    }

# Emergency contacts per region
EMERGENCY_VET_CONTACT = {
    'Nigeria': '+234XXXXXXXXXX',
    'Kenya': '+254XXXXXXXXX',
    'Uganda': '+256XXXXXXXXX',
    'Other': 'N/A'
}

# Symptom logger file (stored locally)
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

# List of diseases with criteria
DISEASES = [
    {
        'key': 'fmd',
        'name': 'Foot-and-Mouth Disease (FMD)',
        'summary': 'Viral; fever, drooling, mouth & hoof blisters.',
        'images': ['images/fmd_mouth.jpg', 'images/fmd_foot.jpg'],
        'criteria': [
            {'question': 'Is the cow drooling excessively or foaming at the mouth?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you observe blisters or raw ulcers in the cow’s mouth?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow limping or reluctant to move with hoof lesions?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have multiple animals in the herd shown similar signs?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Was there recent animal movement or reported outbreaks nearby?', 'options': ['Yes', 'No', 'Not sure'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'cbpp',
        'name': 'Contagious Bovine Pleuropneumonia (CBPP)',
        'summary': 'Bacterial lung disease; painful cough, dyspnea.',
        'images': ['images/cbpp_cough.jpg', 'images/cbpp_pleura.jpg'],
        'criteria': [
            {'question': 'Is the cow coughing persistently with a deep, painful cough?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow showing labored or painful breathing?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Does the cow grunt or react in pain when pressing its ribs?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there a thick or blood-stained nasal discharge?', 'options': ['Thick', 'Clear', 'None'], 'positive': ['Thick']},
            {'question': 'Has the cow been ill for weeks and are others affected?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the herd unvaccinated in an endemic region?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'trypanosomiasis',
        'name': 'Trypanosomiasis (Nagana)',
        'summary': 'Parasitic; intermittent fever, anemia, weight loss.',
        'images': ['images/nagana_anemia.jpg', 'images/tsetse_fly.jpg'],
        'criteria': [
            {'question': 'Has the cow been losing weight steadily over weeks?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are the cow’s eyes or gums pale or white?', 'options': ['Yes', 'No', 'Not sure'], 'positive': ['Yes']},
            {'question': 'Has the cow had intermittent fever episodes?', 'options': ['Yes', 'No', 'Unknown'], 'positive': ['Yes']},
            {'question': 'Does the cow appear weak or lethargic?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do you feel swollen lymph nodes or bottle jaw?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the farm in a tsetse fly area or traveled through one?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'lsd',
        'name': 'Lumpy Skin Disease (LSD)',
        'summary': 'Viral; firm skin nodules, fever, lymph node enlargement.',
        'images': ['images/lsd_nodules.jpg', 'images/lsd_lymph.jpg'],
        'criteria': [
            {'question': 'Does the animal have multiple firm skin nodules?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Did fever precede nodule appearance?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are nodules painful and 1–5 cm in size?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have other cattle developed similar lumps?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there tearing of eyes or nasal discharge?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Has the area had recent LSD outbreaks or new arrivals?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'babesiosis',
        'name': 'Babesiosis (Redwater)',
        'summary': 'Tick-borne; red urine, fever, anemia.',
        'images': ['images/babesiosis_urine.jpg', 'images/blue_tick.jpg'],
        'criteria': [
            {'question': 'Have you observed red or dark urine?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Does the cow have high fever (40–42°C)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are eyes or gums pale or yellow?', 'options': ['Pale', 'Yellow', 'Normal'], 'positive': ['Pale', 'Yellow']},
            {'question': 'Is the cow weak or isolating from herd?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are ticks present on the cow?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is this an adult or newly introduced animal?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'anaplasmosis',
        'name': 'Anaplasmosis',
        'summary': 'Tick-borne; anemia, fever, no red urine.',
        'images': ['images/anaplasmosis_jaundice.jpg'],
        'criteria': [
            {'question': 'Does the cow have high fever (~41°C)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the urine normal color (no redwater)?', 'options': ['Normal', 'Red'], 'positive': ['Normal']},
            {'question': 'Are mucous membranes pale or yellow?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the cow weak or breathless on exertion?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the sick animal an adult (>2 years)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are ticks present or area endemic?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'ecf',
        'name': 'East Coast Fever (ECF)',
        'summary': 'Theileria; swollen nodes, high fever, dyspnea.',
        'images': ['images/ecf_nodes.jpg'],
        'criteria': [
            {'question': 'Are you in an ECF-endemic region?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Does the animal have swollen lymph nodes near the ear or shoulder?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is the fever very high and persistent?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Has the animal developed breathing difficulty?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there tearing of eyes or nasal discharge?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are brown ear ticks visible on the animal?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'brucellosis',
        'name': 'Brucellosis',
        'summary': 'Reproductive; late-term abortion, retained placenta.',
        'images': ['images/brucellosis_abortion.jpg'],
        'criteria': [
            {'question': 'Has the cow aborted in the last trimester?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Did the cow retain the placenta after birth or abortion?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have multiple cows aborted or delivered weak calves?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Do any cattle have painless joint swellings (hygromas)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Have any bulls shown swollen testicles?', 'options': ['Yes', 'No', 'No bulls'], 'positive': ['Yes']},
            {'question': 'Have farm workers reported undulating fevers?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'blackleg',
        'name': 'Blackleg',
        'summary': 'Clostridial; sudden death in young cattle, gas gangrene.',
        'images': ['images/blackleg_swelling.jpg'],
        'criteria': [
            {'question': 'Was a young animal (6–24 months) found dead suddenly?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Was there swelling in a limb or muscle before death?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Could you feel crackling gas under the skin?', 'options': ['Yes', 'No', 'Not checked'], 'positive': ['Yes']},
            {'question': 'Did the animal have fever and depression if observed?', 'options': ['Yes', 'No', 'Not observed'], 'positive': ['Yes']},
            {'question': 'Have other young cattle died suddenly under similar conditions?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Was there recent soil disturbance or handling that could bruise animals?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    },
    {
        'key': 'parasites',
        'name': 'Parasitic Gastroenteritis (Worms)',
        'summary': 'Helminthiasis; poor condition, diarrhea, anemia.',
        'images': ['images/bottle_jaw.jpg'],
        'criteria': [
            {'question': 'Are young cattle losing weight or in poor condition despite feeding?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is there diarrhea or loose stools in the herd?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are mucous membranes pale and is bottle jaw present?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are calves and yearlings more affected than adults?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Is pasture wet or animals rarely dewormed?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
            {'question': 'Are any cattle coughing (possible lungworm)?', 'options': ['Yes', 'No'], 'positive': ['Yes']},
        ]
    }
]

# Streamlit diagnostic UI functions

def run_diagnosis_for(disease):
    st.subheader(disease['name'])
    responses = {}
    match = True
    for c in disease['criteria']:
        choice = st.radio(c['question'], c['options'], key=disease['key']+c['question'])
        responses[c['question']] = choice
        if choice not in c['positive']:
            match = False
    log_symptoms(disease['key'], responses)
    return match

# Main App

def main():
    st.title("🐄 Cattle Health Diagnostic App")
    init_log()
    # Region selection
    region = st.selectbox("Select your region:", list(EMERGENCY_VET_CONTACT.keys()))
    st.write("---")
    # Disease selection
    selected = st.multiselect("Pick diseases to check (or leave blank to check all):",
                              [d['name'] for d in DISEASES], default=None)

    if st.button("Run Diagnosis"):
        results = []
        for disease in DISEASES:
            if not selected or disease['name'] in selected:
                if run_diagnosis_for(disease):
                    results.append(disease)
        if results:
            # Show first match
            diag = results[0]
            st.success(f"Likely diagnosis: {diag['name']}")
            st.write(diag['summary'])
            for img in diag['images']:
                st.image(img, use_column_width=True)
            st.info(f"Emergency vet contact for {region}: {EMERGENCY_VET_CONTACT[region]}")
        else:
            st.error("No matching diagnosis found. Please consult a veterinarian.")

if __name__ == '__main__':
    main()
```
