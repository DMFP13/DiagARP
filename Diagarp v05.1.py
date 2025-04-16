# Diagarp Streamlit App – Full-width UI with Ranked Diagnosis Output

import streamlit as st
from typing import List

st.set_page_config(page_title="Diagarp Cattle Diagnosis", layout="wide", page_icon="🐄")
st.title("🐄 Diagarp: Cattle Disease Diagnostic Tool")
st.markdown("Diagnose common cattle health issues using a structured, symptom-based decision tree.")

# --- Embedded Decision Tree ---
decision_tree = {
    "start": {
        "question": "What is the primary symptom observed?",
        "options": {
            "Weakness or lethargy": "q1",
            "Coughing or laboured breathing": "brd_path",
            "Diarrhoea": "q7",
            "Lameness or foot/mouth issues": "q6a",
            "Weight loss or poor condition": "q3",
            "Eye discharge or cloudiness": "eye_path",
            "Nervous signs (tremors, aggression)": "q4",
            "Recumbency or inability to stand": "q5",
            "Other/Unclear": "context_environment"
        }
    },

    # Enhanced BRD branch
    "brd_path": {
        "question": "Was there a recent stress event (e.g., transport, weaning)?",
        "yes": "brd_final",
        "no": "brd_other_causes"
    },
    "brd_other_causes": {
        "question": "Is there fever, rapid breathing, or abnormal lung sounds?",
        "yes": "brd_final",
        "no": "unknown_final"
    },

    # Eye issues path
    "eye_path": {
        "question": "Is the eye cloudy, ulcerated, or swollen shut?",
        "yes": "ibk_final",
        "no": "eye_irritation"
    },
    "eye_irritation": {
        "diagnosis": "Possible trauma or irritant (dust, hay seed, sunlight)",
        "likelihood": 40,
        "treatment": "Flush eye with clean water or saline. Apply eye ointment if available.",
        "prevention": "Reduce dust and bright sunlight exposure. Provide shelter/shade."
    },

    # Enhanced Lameness / Mouth Issues Path
    "q6a": {
        "question": "Is there swelling or discharge around the hooves or between claws?",
        "yes": "foot_rot_final",
        "no": "q6b"
    },
    "q6b": {
        "question": "Are there ulcers, blisters, or salivation indicating oral lesions?",
        "yes": "fmd_final",
        "no": "q6c"
    },
    "q6c": {
        "question": "Is the animal reluctant to rise or appears stiff in multiple joints?",
        "yes": "arthritis_consideration",
        "no": "unknown_final"
    },

    "arthritis_consideration": {
        "diagnosis": "Possible infectious arthritis or foot lameness",
        "likelihood": 50,
        "treatment": "Consult a veterinarian. Joint taps or antimicrobial therapy may be required depending on the cause.",
        "prevention": "Maintain good hygiene in calving and housing areas. Monitor for early signs of joint swelling."
    },

    # Weight Loss Path (expanded)
    "q3": {
        "question": "Is the appetite normal?",
        "yes": "q3a",
        "no": "parasitic_final"
    },
    "q3a": {
        "question": "Has the condition developed slowly over months?",
        "yes": "johnes_final",
        "no": "stress_related_final"
    },

    # Recumbent Path (expanded)
    "q5": {
        "question": "Is the cow alert but unable to stand?",
        "yes": "q5a",
        "no": "hardware_disease_final"
    },
    "q5a": {
        "question": "Has the cow calved within the last 72 hours?",
        "yes": "milk_fever_final",
        "no": "neurological_consult"
    },

    # Contextual and Environmental Factors
    "context_environment": {
        "question": "Have there been recent weather changes, stress, or diet transitions?",
        "yes": "stress_related_final",
        "no": "region_check"
    },
    "region_check": {
        "question": "Is this farm in a tropical or high parasite region?",
        "yes": "parasitic_final",
        "no": "unknown_final"
    },

    # Appetite & Weakness Path
    "q1": {
        "question": "Is there a noticeable loss of appetite?",
        "yes": "q2",
        "no": "pica_final"
    },
    "q2": {
        "question": "Is the cow losing weight despite eating?",
        "yes": "ketosis_final",
        "no": "milk_fever_final"
    },

    # Nervous Signs Path
    "q4": {
        "question": "Has the cow recently calved?",
        "yes": "nervous_ketosis_final",
        "no": "rabies_check"
    },
    "rabies_check": {
        "question": "Is the cow showing unusual aggression or biting objects?",
        "yes": "rabies_final",
        "no": "neurological_consult"
    },

    # Diarrhoea Path
    "q7": {
        "question": "Is the diarrhoea chronic (>2 weeks)?",
        "yes": "johnes_final",
        "no": "q8"
    },
    "q8": {
        "question": "Is the cow under 6 months old?",
        "yes": "coccidiosis_final",
        "no": "bvd_final"
    },

    # Final diagnoses (with likelihood tags added)
    "brd_final": {
        "diagnosis": "Bovine Respiratory Disease (BRD)",
        "likelihood": 85,
        "treatment": "Administer long-acting antibiotics and NSAIDs. Ensure good ventilation and reduce stress.",
        "prevention": "Vaccinate against respiratory pathogens and avoid overcrowding and stress."
    },
    "ketosis_final": {
        "diagnosis": "Ketosis (Acetonemia)",
        "likelihood": 70,
        "treatment": "Provide oral propylene glycol and IV dextrose. Adjust dietary energy.",
        "prevention": "Monitor fresh cows and ensure energy-rich diet pre- and post-calving."
    },
    "milk_fever_final": {
        "diagnosis": "Milk Fever (Hypocalcemia)",
        "likelihood": 75,
        "treatment": "IV calcium borogluconate. Monitor cardiac function and keep cow warm.",
        "prevention": "Manage calcium intake. Administer oral calcium supplements at calving."
    },
    "pica_final": {
        "diagnosis": "Pica (Mineral Deficiency)",
        "likelihood": 60,
        "treatment": "Supplement missing minerals (P, Na). Provide mineral blocks and clean water.",
        "prevention": "Regular forage analysis and balanced mineral supplementation."
    },
    "johnes_final": {
        "diagnosis": "Johne’s Disease",
        "likelihood": 65,
        "treatment": "No effective treatment. Cull affected animals. Maintain hygiene.",
        "prevention": "Test-and-cull, pasteurize colostrum, and separate calves from adult manure."
    },
    "parasitic_final": {
        "diagnosis": "Parasitic Infection (worms or liver fluke)",
        "likelihood": 60,
        "treatment": "Administer broad-spectrum anthelmintics. Consider liver fluke specific agents.",
        "prevention": "Rotational grazing and fecal testing. Deworm strategically."
    },
    "nervous_ketosis_final": {
        "diagnosis": "Nervous Ketosis",
        "likelihood": 55,
        "treatment": "IV dextrose, corticosteroids, and oral propylene glycol. Handle with caution.",
        "prevention": "Monitor high-risk cows for negative energy balance early post-calving."
    },
    "rabies_final": {
        "diagnosis": "Rabies",
        "likelihood": 30,
        "treatment": "No treatment. Euthanize and contact authorities. Zoonotic risk.",
        "prevention": "Vaccinate in endemic regions. Avoid exposure to wild animals."
    },
    "neurological_consult": {
        "diagnosis": "Neurological disorder (unspecified)",
        "likelihood": 40,
        "treatment": "Seek veterinary advice. Test for listeriosis, polioencephalomalacia, etc.",
        "prevention": "Prevent silage spoilage. Supplement thiamine and monitor closely."
    },
    "hardware_disease_final": {
        "diagnosis": "Hardware Disease",
        "likelihood": 50,
        "treatment": "Administer magnet and antibiotics. May require surgery.",
        "prevention": "Use rumen magnets and control metallic debris in feed areas."
    },
    "fmd_final": {
        "diagnosis": "Foot-and-Mouth Disease (FMD)",
        "likelihood": 45,
        "treatment": "Isolate. Provide soft food, antibiotics for secondary infections, and pain relief.",
        "prevention": "Vaccinate and enforce strict biosecurity. Notify authorities."
    },
    "foot_rot_final": {
        "diagnosis": "Foot Rot",
        "likelihood": 70,
        "treatment": "Clean and debride foot. Administer systemic antibiotics.",
        "prevention": "Foot bathing, dry conditions, and early detection."
    },
    "coccidiosis_final": {
        "diagnosis": "Coccidiosis",
        "likelihood": 60,
        "treatment": "Use sulfa drugs or amprolium. Isolate and rehydrate affected calves.",
        "prevention": "Keep housing clean and dry. Use medicated feed preventively."
    },
    "bvd_final": {
        "diagnosis": "Bovine Viral Diarrhea (BVD)",
        "likelihood": 55,
        "treatment": "Supportive care only. Isolate infected animals.",
        "prevention": "Vaccination program and removal of persistently infected animals."
    },
    "ibk_final": {
        "diagnosis": "Infectious Bovine Keratoconjunctivitis (Pinkeye)",
        "likelihood": 70,
        "treatment": "Topical or injectable antibiotics. Provide shade and fly protection.",
        "prevention": "Fly control, pasture management, and vaccination."
    },
    "stress_related_final": {
        "diagnosis": "Stress-related syndrome (unspecified)",
        "likelihood": 40,
        "treatment": "Monitor closely. Provide supportive care, minimize handling, and offer clean water/feed.",
        "prevention": "Avoid abrupt diet changes and stressful conditions. Allow acclimatization during seasonal shifts."
    },
    "unknown_final": {
        "diagnosis": "Diagnosis unclear",
        "likelihood": 10,
        "treatment": "Consult a veterinarian for further examination.",
        "prevention": "Continue regular monitoring and record-keeping."
    }

# --- Utility Function ---
def get_likely_diagnoses(tree):
    diagnoses = []
    for node in tree.values():
        if isinstance(node, dict) and "diagnosis" in node and "likelihood" in node:
            diagnoses.append((
                node["diagnosis"],
                node["likelihood"],
                node.get("treatment", ""),
                node.get("prevention", "")
            ))
    return sorted(diagnoses, key=lambda x: x[1], reverse=True)

# --- Initialize Session State ---
if "step" not in st.session_state:
    st.session_state.step = "start"
    st.session_state.history = []
    st.session_state.answers = []
    st.session_state.complete = False

# --- Sidebar Tracker ---
st.sidebar.header("📝 Diagnosis Progress")
if st.session_state.answers:
    for idx, item in enumerate(st.session_state.answers):
        st.sidebar.markdown(f"**Step {idx + 1}:** {item}")
else:
    st.sidebar.info("No answers selected yet.")

# --- Diagnosis Completed ---
if st.session_state.complete:
    st.success("Diagnosis complete.")
    st.subheader("🔎 Top Likely Diagnoses")
    top_diagnoses = get_likely_diagnoses(decision_tree)
    for diagnosis, likelihood, treatment, prevention in top_diagnoses[:3]:
        with st.container():
            st.markdown(f"### ✅ {diagnosis} ({likelihood}% likelihood)")
            st.markdown(f"**💊 Treatment:** {treatment}")
            st.markdown(f"**🛡️ Prevention:** {prevention}")
            st.markdown("---")
    if st.button("🔁 Start Over"):
        for key in ["step", "history", "answers", "complete"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()

# --- Navigation Logic ---
else:
    node = decision_tree[st.session_state.step]

    with st.form(key="diagnosis_form"):
        st.markdown(f"## {node['question']}")

        if "options" in node:
            user_input = st.radio("Select an option:", list(node["options"].keys()))
        else:
            user_input = st.radio("Select one:", ["Yes", "No"])

        submitted = st.form_submit_button("Next")

        if submitted:
            st.session_state.answers.append(f"{node['question']} → {user_input}")
            st.session_state.history.append(st.session_state.step)

            if "options" in node:
                next_step = node["options"][user_input]
            else:
                next_step = node["yes"] if user_input == "Yes" else node["no"]

            st.session_state.step = next_step
            if "diagnosis" in decision_tree.get(next_step, {}):
                st.session_state.complete = True
            st.experimental_rerun()

# ✅ The full decision_tree content from canvas should now be pasted directly below or in place of the placeholder import.
# You can paste the decision_tree definition starting with: decision_tree = { ... } from your final validated version.
