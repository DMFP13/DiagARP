import streamlit as st

st.set_page_config(page_title="Diagarp Cattle Diagnosis", page_icon="🐄")
st.title("🐄 Diagarp: Cattle Disease Diagnostic Tool")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "start"
    st.session_state.symptom_log = []
    st.session_state.diagnosed = False

# Enhanced Diagarp Decision Tree with Combined Logic and Contextual Nodes
# This version merges detailed symptom-based branching with binary yes/no format,
# and includes diagnosis, treatment, prevention, and environmental/contextual logic.

decision_tree = {
    "start": {
        "question": "What is the primary symptom observed?",
        "options": {
            "Weakness or lethargy": "q1",
            "Coughing or laboured breathing": "brd_final",
            "Diarrhoea": "q7",
            "Lameness or foot/mouth issues": "q6",
            "Weight loss or poor condition": "q3",
            "Eye discharge or cloudiness": "ibk_final",
            "Nervous signs (tremors, aggression)": "q4",
            "Recumbency or inability to stand": "q5",
            "Other/Unclear": "context_environment"
        }
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

    # Appetite & Weight Loss
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

    # Weight Loss Path
    "q3": {
        "question": "Is the appetite normal?",
        "yes": "johnes_final",
        "no": "parasitic_final"
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

    # Recumbent
    "q5": {
        "question": "Is the cow alert but unable to stand?",
        "yes": "milk_fever_final",
        "no": "hardware_disease_final"
    },

    # Lameness or Mouth Issues
    "q6": {
        "question": "Are there blisters on the feet or mouth?",
        "yes": "fmd_final",
        "no": "foot_rot_final"
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

    # Diagnoses
    "brd_final": {
        "diagnosis": "Bovine Respiratory Disease (BRD)",
        "treatment": "Administer long-acting antibiotics and NSAIDs. Ensure good ventilation and reduce stress.",
        "prevention": "Vaccinate against respiratory pathogens and avoid overcrowding and stress."
    },
    "ketosis_final": {
        "diagnosis": "Ketosis (Acetonemia)",
        "treatment": "Provide oral propylene glycol and IV dextrose. Adjust dietary energy.",
        "prevention": "Monitor fresh cows and ensure energy-rich diet pre- and post-calving."
    },
    "milk_fever_final": {
        "diagnosis": "Milk Fever (Hypocalcemia)",
        "treatment": "IV calcium borogluconate. Monitor cardiac function and keep cow warm.",
        "prevention": "Manage calcium intake. Administer oral calcium supplements at calving."
    },
    "pica_final": {
        "diagnosis": "Pica (Mineral Deficiency)",
        "treatment": "Supplement missing minerals (P, Na). Provide mineral blocks and clean water.",
        "prevention": "Regular forage analysis and balanced mineral supplementation."
    },
    "johnes_final": {
        "diagnosis": "Johne’s Disease",
        "treatment": "No effective treatment. Cull affected animals. Maintain hygiene.",
        "prevention": "Test-and-cull, pasteurize colostrum, and separate calves from adult manure."
    },
    "parasitic_final": {
        "diagnosis": "Parasitic Infection (worms or liver fluke)",
        "treatment": "Administer broad-spectrum anthelmintics. Consider liver fluke specific agents.",
        "prevention": "Rotational grazing and fecal testing. Deworm strategically."
    },
    "nervous_ketosis_final": {
        "diagnosis": "Nervous Ketosis",
        "treatment": "IV dextrose, corticosteroids, and oral propylene glycol. Handle with caution.",
        "prevention": "Monitor high-risk cows for negative energy balance early post-calving."
    },
    "rabies_final": {
        "diagnosis": "Rabies",
        "treatment": "No treatment. Euthanize and contact authorities. Zoonotic risk.",
        "prevention": "Vaccinate in endemic regions. Avoid exposure to wild animals."
    },
    "neurological_consult": {
        "diagnosis": "Neurological disorder (unspecified)",
        "treatment": "Seek veterinary advice. Test for listeriosis, polioencephalomalacia, etc.",
        "prevention": "Prevent silage spoilage. Supplement thiamine and monitor closely."
    },
    "hardware_disease_final": {
        "diagnosis": "Hardware Disease",
        "treatment": "Administer magnet and antibiotics. May require surgery.",
        "prevention": "Use rumen magnets and control metallic debris in feed areas."
    },
    "fmd_final": {
        "diagnosis": "Foot-and-Mouth Disease (FMD)",
        "treatment": "Isolate. Provide soft food, antibiotics for secondary infections, and pain relief.",
        "prevention": "Vaccinate and enforce strict biosecurity. Notify authorities."
    },
    "foot_rot_final": {
        "diagnosis": "Foot Rot",
        "treatment": "Clean and debride foot. Administer systemic antibiotics.",
        "prevention": "Foot bathing, dry conditions, and early detection."
    },
    "coccidiosis_final": {
        "diagnosis": "Coccidiosis",
        "treatment": "Use sulfa drugs or amprolium. Isolate and rehydrate affected calves.",
        "prevention": "Keep housing clean and dry. Use medicated feed preventively."
    },
    "bvd_final": {
        "diagnosis": "Bovine Viral Diarrhea (BVD)",
        "treatment": "Supportive care only. Isolate infected animals.",
        "prevention": "Vaccination program and removal of persistently infected animals."
    },
    "ibk_final": {
        "diagnosis": "Infectious Bovine Keratoconjunctivitis (Pinkeye)",
        "treatment": "Topical or injectable antibiotics. Provide shade and fly protection.",
        "prevention": "Fly control, pasture management, and vaccination."
    },
    "stress_related_final": {
        "diagnosis": "Stress-related syndrome (unspecified)",
        "treatment": "Monitor closely. Provide supportive care, minimize handling, and offer clean water/feed.",
        "prevention": "Avoid abrupt diet changes and stressful conditions. Allow acclimatization during seasonal shifts."
    },
    "unknown_final": {
        "diagnosis": "Diagnosis unclear",
        "treatment": "Consult a veterinarian for further examination.",
        "prevention": "Continue regular monitoring and record-keeping."
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
