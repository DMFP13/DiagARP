import streamlit as st

st.set_page_config(page_title="Diagarp Cattle Diagnosis", page_icon="🐄")
st.title("🐄 Diagarp: Cattle Disease Diagnostic Tool")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "start"
    st.session_state.symptom_log = []
    st.session_state.diagnosed = False

# Decision tree structure
decision_tree = {
    "start": {
        "question": "Is the cow showing signs of weakness or lethargy?",
        "yes": "q1",
        "no": "q2"
    },
    "q1": {
        "question": "Is there a noticeable loss of appetite?",
        "yes": "q3",
        "no": "q4"
    },
    "q2": {
        "question": "Is the cow coughing or has nasal discharge?",
        "yes": "brd_final",
        "no": "q5"
    },
    "q3": {
        "question": "Is the cow losing weight despite eating?",
        "yes": "ketosis_final",
        "no": "q4"
    },
    "q4": {
        "question": "Is the cow showing muscle tremors, especially after calving?",
        "yes": "fever_final",
        "no": "q5"
    },
    "q5": {
        "question": "Is the cow chewing on non-food items (e.g., soil, wood)?",
        "yes": "pica_final",
        "no": "q6"
    },
    "q6": {
        "question": "Is the cow showing signs of lameness or blisters on the feet or mouth?",
        "yes": "fmd_final",
        "no": "q7"
    },
    "q7": {
        "question": "Is the cow having diarrhea with fever or mouth ulcers?",
        "yes": "bvd_final",
        "no": "q8"
    },
    "q8": {
        "question": "Is there jaundice or signs of anemia (pale eyes, weakness)?",
        "yes": "anaplasmosis_final",
        "no": "q9"
    },
    "q9": {
        "question": "Is there evidence of eye discharge or blindness?",
        "yes": "ibk_final",
        "no": "unknown_final"
    },
    "brd_final": {
        "diagnosis": "Bovine Respiratory Disease (BRD)",
        "treatment": "Administer antibiotics and anti-inflammatory drugs. Ensure good ventilation and reduce stress.",
        "prevention": "Vaccinate against respiratory pathogens and avoid overcrowding."
    },
    "ketosis_final": {
        "diagnosis": "Ketosis (Acetonemia)",
        "treatment": "Provide oral glucose precursors and intravenous dextrose. Monitor energy intake.",
        "prevention": "Ensure adequate energy levels pre- and post-calving."
    },
    "fever_final": {
        "diagnosis": "Milk Fever (Hypocalcemia)",
        "treatment": "Administer calcium borogluconate intravenously. Keep the cow warm and monitor closely.",
        "prevention": "Manage calcium intake before and after calving. Use calcium supplements as needed."
    },
    "pica_final": {
        "diagnosis": "Pica (Mineral Deficiency)",
        "treatment": "Supplement minerals like phosphorus and provide access to salt licks.",
        "prevention": "Ensure mineral supplementation and balanced diet."
    },
    "fmd_final": {
        "diagnosis": "Foot-and-Mouth Disease (FMD)",
        "treatment": "Isolate affected animals. Provide soft food and pain relief.",
        "prevention": "Regular vaccination and biosecurity control."
    },
    "bvd_final": {
        "diagnosis": "Bovine Viral Diarrhea (BVD)",
        "treatment": "Supportive care and isolate infected animals.",
        "prevention": "Vaccination and regular herd testing."
    },
    "anaplasmosis_final": {
        "diagnosis": "Anaplasmosis",
        "treatment": "Treat with tetracyclines under vet supervision. Provide supportive care.",
        "prevention": "Control ticks and consider vaccination where available."
    },
    "ibk_final": {
        "diagnosis": "Infectious Bovine Keratoconjunctivitis (Pinkeye)",
        "treatment": "Apply topical antibiotics. Protect eyes from sunlight and flies.",
        "prevention": "Fly control, vaccination, and reduce eye irritants."
    },
    "unknown_final": {
        "diagnosis": "Diagnosis unclear.",
        "treatment": "Consult a veterinarian for a detailed examination.",
        "prevention": "Monitor health regularly and maintain records."
    }
}

# If diagnosis reached, show result
if st.session_state.diagnosed:
    result = decision_tree[st.session_state.step]
    st.subheader(f"🩺 Diagnosis: {result['diagnosis']}")
    st.markdown(f"**💊 Treatment:** {result['treatment']}")
    st.markdown(f"**🛡️ Prevention:** {result['prevention']}")
    if st.button("🔁 Restart Diagnosis"):
        st.session_state.step = "start"
        st.session_state.symptom_log = []
        st.session_state.diagnosed = False
else:
    node = decision_tree[st.session_state.step]
    with st.form("diagarp_form"):
        st.markdown(f"**{node['question']}**")
        answer = st.radio("Choose one:", ["Yes", "No"])
        submitted = st.form_submit_button("Next")

        if submitted:
            if answer == "Yes":
                st.session_state.symptom_log.append(node["question"])
                st.session_state.step = node["yes"]
            else:
                st.session_state.step = node["no"]

            if "final" in st.session_state.step:
                st.session_state.diagnosed = True
