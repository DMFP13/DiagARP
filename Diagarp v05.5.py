# Diagarp Streamlit App – Full-width UI with Ranked Diagnosis Output

import streamlit as st
from typing import List

st.set_page_config(page_title="Diagarp Cattle Diagnosis", layout="wide", page_icon="🐄")
st.markdown("""
    <h1 style='font-size: 3em; color: #2c3e50; font-weight: bold;'>🐄 Diagarp: Cattle Disease Diagnostic Tool</h1>
""", unsafe_allow_html=True)
st.markdown("""
<div style='font-size:1.2em; color:#555;'>
    Use this tool to identify likely cattle diseases based on symptom paths, and receive treatment and prevention advice.
</div>
""", unsafe_allow_html=True)

# --- Embedded Decision Tree ---
decision_tree = {
    "start": {
        "question": "What is the primary symptom observed?",
        "options": {
            "Weakness or lethargy": "weakness_q1",
            "Coughing or laboured breathing": "brd_q1",
            "Diarrhoea": "diarrhea_q1",
            "Lameness or foot/mouth issues": "lameness_q1",
            "Weight loss or poor condition": "weightloss_q1",
            "Eye discharge or cloudiness": "eye_q1",
            "Nervous signs (tremors, aggression)": "nervous_q1",
            "Recumbency or inability to stand": "recumbent_q1",
            "Other/Unclear": "context_q1"
        }
    },
    "weakness_q1": {
        "question": "Is the cow eating normally?",
        "yes": "weakness_q2",
        "no": "weakness_q3"
    },
    "weakness_q2": {
        "question": "Is there any sign of mineral deficiency (e.g. chewing soil)?",
        "yes": "pica_final",
        "no": "unknown_final"
    },
    "weakness_q3": {
        "question": "Has the cow recently calved?",
        "yes": "milk_fever_final",
        "no": "ketosis_final"
    },
    "brd_q1": {
        "question": "Is there nasal discharge?",
        "yes": "brd_q2",
        "no": "brd_q2"
    },
    "brd_q2": {
        "question": "Is there fever?",
        "yes": "brd_q3",
        "no": "brd_q3"
    },
    "brd_q3": {
        "question": "Is appetite decreased?",
        "yes": "brd_q4",
        "no": "brd_q4"
    },
    "brd_q4": {
        "question": "Has there been recent stress or transport?",
        "yes": "brd_final",
        "no": "brd_final"
    },
    "brd_final": {
        "diagnosis": "Bovine Respiratory Disease (BRD)",
        "likelihood": 85,
        "treatment": "Administer long-acting antibiotics and NSAIDs. Ensure good ventilation and reduce stress.",
        "prevention": "Vaccinate against respiratory pathogens and avoid overcrowding and stress."
    },
    "milk_fever_final": {
        "diagnosis": "Milk Fever (Hypocalcemia)",
        "likelihood": 75,
        "treatment": "IV calcium borogluconate. Monitor cardiac function and keep cow warm.",
        "prevention": "Manage calcium intake. Administer oral calcium supplements at calving."
    },
    "ketosis_final": {
        "diagnosis": "Ketosis (Acetonemia)",
        "likelihood": 70,
        "treatment": "Provide oral propylene glycol and IV dextrose. Adjust dietary energy.",
        "prevention": "Monitor fresh cows and ensure energy-rich diet pre- and post-calving."
    },
    "pica_final": {
        "diagnosis": "Pica (Mineral Deficiency)",
        "likelihood": 60,
        "treatment": "Supplement missing minerals (P, Na). Provide mineral blocks and clean water.",
        "prevention": "Regular forage analysis and balanced mineral supplementation."
    },
    "diarrhea_q1": {
        "question": "Is the diarrhea watery and persistent?",
        "yes": "bvd_q1",
        "no": "coccidiosis_q1"
    },
    "lameness_q1": {
        "question": "Is the lameness localized to a single limb?",
        "yes": "footrot_q1",
        "no": "fmd_q1"
    },
    "weightloss_q1": {
        "question": "Is appetite normal despite weight loss?",
        "yes": "johnes_q1",
        "no": "ketosis_final"
    },
    "eye_q1": {
        "question": "Is there ulceration or cloudiness in the eye?",
        "yes": "ibk_final",
        "no": "unknown_final"
    },
    "nervous_q1": {
        "question": "Is the cow showing signs of circling or head pressing?",
        "yes": "neurological_final",
        "no": "unknown_final"
    },
    "recumbent_q1": {
        "question": "Is the cow alert but unable to rise?",
        "yes": "milk_fever_final",
        "no": "unknown_final"
    },
    "context_q1": {
        "question": "Have there been recent changes in weather or feed?",
        "yes": "stress_related_final",
        "no": "unknown_final"
    },
    "bvd_q1": {
        "question": "Is the cow experiencing diarrhea and fever?",
        "yes": "bvd_q2",
        "no": "unknown_final"
    },
    "bvd_q2": {
        "question": "Is the animal less than 24 months old?",
        "yes": "bvd_q3",
        "no": "unknown_final"
    },
    "bvd_q3": {
        "question": "Is there evidence of immunosuppression (e.g., secondary infections)?",
        "yes": "bvd_q4",
        "no": "unknown_final"
    },
    "bvd_q4": {
        "question": "Has the animal had close contact with persistently infected animals?",
        "yes": "bvd_q5",
        "no": "unknown_final"
    },
    "bvd_q5": {
        "question": "Was the animal vaccinated against BVD?",
        "yes": "unknown_final",
        "no": "bvd_final"
    },
    "bvd_final": {
        "diagnosis": "Bovine Viral Diarrhea (BVD)",
        "likelihood": 65,
        "treatment": "Supportive care only. Isolate infected animals.",
        "prevention": "Vaccination program and removal of persistently infected animals."
    },
    "coccidiosis_q1": {
        "question": "Is the calf under 6 months of age?",
        "yes": "coccidiosis_q2",
        "no": "unknown_final"
    },
    "coccidiosis_q2": {
        "question": "Is there watery or bloody diarrhea?",
        "yes": "coccidiosis_q3",
        "no": "unknown_final"
    },
    "coccidiosis_q3": {
        "question": "Is the calf weak and dehydrated?",
        "yes": "coccidiosis_q4",
        "no": "unknown_final"
    },
    "coccidiosis_q4": {
        "question": "Has the calf recently experienced stress (e.g. weaning)?",
        "yes": "coccidiosis_q5",
        "no": "unknown_final"
    },
    "coccidiosis_q5": {
        "question": "Is the environment dirty or overcrowded?",
        "yes": "coccidiosis_final",
        "no": "unknown_final"
    },
    "coccidiosis_final": {
        "diagnosis": "Coccidiosis",
        "likelihood": 70,
        "treatment": "Use sulfa drugs or amprolium. Isolate and rehydrate affected calves.",
        "prevention": "Keep housing clean and dry. Use medicated feed preventively."
    },
    "ibk_final": {
        "diagnosis": "Infectious Bovine Keratoconjunctivitis (Pinkeye)",
        "likelihood": 60,
        "treatment": "Apply topical antibiotics. Protect eyes from sunlight and flies.",
        "prevention": "Fly control, vaccination, and reduce eye irritants."
    },
    "neurological_final": {
        "diagnosis": "Neurological disorder (Listeriosis or Polioencephalomalacia)",
        "likelihood": 55,
        "treatment": "Seek veterinary advice. Administer thiamine and antibiotics where appropriate.",
        "prevention": "Avoid spoiled silage and ensure proper vitamin supplementation."
    },
    "stress_related_final": {
        "diagnosis": "Stress-related illness",
        "likelihood": 45,
        "treatment": "Supportive care. Reduce environmental and management stressors.",
        "prevention": "Avoid abrupt changes in feed or housing. Maintain consistent routines."
    },
    "unknown_final": {
        "diagnosis": "Diagnosis unclear",
        "likelihood": 10,
        "treatment": "Consult a veterinarian for further examination.",
        "prevention": "Continue regular monitoring and record-keeping."
    }
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
st.sidebar.markdown("""
    <h3 style='color:#1abc9c;'>📝 Diagnosis Progress</h3>
""", unsafe_allow_html=True)
if st.session_state.answers:
    st.sidebar.progress(len(st.session_state.answers) / 5)  # assume 5-step depth typical
    for idx, item in enumerate(st.session_state.answers):
        st.sidebar.markdown(f"**Step {idx + 1}:** {item}")
else:
    st.sidebar.info("No answers selected yet.")

# --- Diagnosis Completed ---
if st.session_state.complete:
    st.markdown("""
<div style='background-color: #e8f8f5; padding: 1em; border-left: 5px solid #1abc9c;'>
    ✅ <strong>Diagnosis complete.</strong> Review your results below.
</div>
""", unsafe_allow_html=True)
    st.markdown("""
<h2 style='color: #2c3e50;'>🔎 Top Likely Diagnoses</h2>
""", unsafe_allow_html=True)
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
        st.rerun()

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
            st.rerun()
