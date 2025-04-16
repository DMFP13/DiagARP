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
            "Lameness or foot/mouth issues": "q6_intro",
            "Weight loss or poor condition": "q3",
            "Eye discharge or cloudiness": "eye_path",
            "Nervous signs (tremors, aggression)": "q4",
            "Recumbency or inability to stand": "q5",
            "Other/Unclear": "context_environment"
        }
    },
    "brd_path": {
        "question": "Is the cow exhibiting coughing or laboured breathing?",
        "yes": "brd_q2",
        "no": "unknown_final"
    },
    "brd_q2": {
        "question": "Is there nasal discharge present?",
        "yes": "brd_q3",
        "no": "brd_q3"
    },
    "brd_q3": {
        "question": "Is the cow running a fever?",
        "yes": "brd_q4",
        "no": "brd_q4"
    },
    "brd_q4": {
        "question": "Has the cow's appetite decreased?",
        "yes": "brd_q5",
        "no": "brd_q5"
    },
    "brd_q5": {
        "question": "Has there been recent transportation or stress?",
        "yes": "brd_final",
        "no": "brd_final"
    },
    "brd_final": {
        "diagnosis": "Bovine Respiratory Disease (BRD)",
        "likelihood": 85,
        "treatment": "Administer long-acting antibiotics and NSAIDs. Ensure good ventilation and reduce stress.",
        "prevention": "Vaccinate against respiratory pathogens and avoid overcrowding and stress."
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
    "pica_q1": {
        "question": "Is the cow eating non-food materials (e.g., wood, dirt)?",
        "yes": "pica_q2",
        "no": "unknown_final"
    },
    "pica_q2": {
        "question": "Is there a known mineral deficiency in the region or diet?",
        "yes": "pica_q3",
        "no": "unknown_final"
    },
    "pica_q3": {
        "question": "Are other animals in the herd displaying similar behavior?",
        "yes": "pica_q4",
        "no": "unknown_final"
    },
    "pica_q4": {
        "question": "Is the feed lacking in phosphorus or sodium?",
        "yes": "pica_q5",
        "no": "unknown_final"
    },
    "pica_q5": {
        "question": "Is the cow’s water source clean and accessible?",
        "yes": "pica_final",
        "no": "unknown_final"
    },
    "pica_final": {
        "diagnosis": "Pica (Mineral Deficiency)",
        "likelihood": 60,
        "treatment": "Supplement missing minerals (P, Na). Provide mineral blocks and clean water.",
        "prevention": "Regular forage analysis and balanced mineral supplementation."
    },
    "q1": {
        "question": "Is there a noticeable loss of appetite?",
        "yes": "unknown_final",
        "no": "unknown_final"
    },
    "q3": {
        "question": "Is the appetite normal?",
        "yes": "unknown_final",
        "no": "unknown_final"
    },
    "q4": {
        "question": "Has the cow recently calved?",
        "yes": "unknown_final",
        "no": "unknown_final"
    },
    "q5": {
        "question": "Is the cow alert but unable to stand?",
        "yes": "unknown_final",
        "no": "unknown_final"
    },
    "q6_intro": {
        "question": "Is the issue located around the feet, mouth, or general stiffness?",
        "options": {
            "Feet (hoof, sole, interdigital)": "unknown_final",
            "Mouth (blisters, drooling, ulcers)": "unknown_final",
            "Stiffness or joint pain": "unknown_final"
        }
    },
    "q7": {
        "question": "Is the diarrhea chronic (>2 weeks)?",
        "yes": "unknown_final",
        "no": "unknown_final"
    },
    "eye_path": {
        "question": "Is the eye cloudy, ulcerated, or swollen shut?",
        "yes": "unknown_final",
        "no": "unknown_final"
    },
    "context_environment": {
        "question": "Have there been recent weather changes, stress, or diet transitions?",
        "yes": "unknown_final",
        "no": "unknown_final"
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
st.sidebar.header("📝 Diagnosis Progress")
if st.session_state.answers:
    st.sidebar.progress(len(st.session_state.answers) / 5)  # assume 5-step depth typical
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
