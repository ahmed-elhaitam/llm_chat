import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage

# Initialiser le modèle ChatGroq
llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    groq_api_key="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",
    temperature=0
)

# Interface utilisateur
st.title("LLM Innovant pour l'Orientation")
st.markdown("**Sélectionnez une école, explorez les formations et découvrez les débouchés professionnels !**")

# Données des écoles et formations
ecoles_formations = {
    "EHTP": ["Génie Civil", "Génie Informatique", "Génie Electrique"],
    "EMI": ["Génie Mécanique", "Génie Informatique", "Génie Industriel"],
    "INPT": ["Data Science", "Cybersecurity", "Telecom Engineering"],
    "ENSIAS": ["Artificial Intelligence", "Software Engineering", "Data Engineering"]
}

debouches_mapping = {
    "Génie Civil": ["Ingénieur Civil, Urbaniste, Gestionnaire de Travaux"],
    "Génie Informatique": ["Développeur Logiciel, Ingénieur Système, Architecte Cloud"],
    "Génie Electrique": ["Ingénieur Électrique, Responsable Maintenance, Consultant Énergie"],
    "Génie Mécanique": ["Ingénieur CAO, Expert en Robotique, Responsable Production"],
    "Génie Industriel": ["Consultant Lean Management, Responsable Logistique"],
    "Data Science": ["Data Scientist, Big Data Analyst, Machine Learning Engineer"],
    "Cybersecurity": ["Analyste Sécurité, Ethical Hacker, Responsable IT"],
    "Telecom Engineering": ["Ingénieur Réseaux, Consultant Télécoms, Architecte Télécom"],
    "Artificial Intelligence": ["AI Developer, Robotics Engineer, Machine Learning Specialist"],
    "Software Engineering": ["Software Developer, Application Architect, DevOps Engineer"],
    "Data Engineering": ["Data Engineer, ETL Developer, Database Administrator"]
}

# Sélection de l'école
selected_ecole = st.selectbox("Choisissez une école :", list(ecoles_formations.keys()))

if selected_ecole:
    # Afficher les formations disponibles
    formations = ecoles_formations[selected_ecole]
    selected_formation = st.selectbox(f"Formations disponibles à {selected_ecole} :", formations)

    if selected_formation:
        # Afficher les débouchés correspondants
        debouches = debouches_mapping.get(selected_formation, ["Débouchés diversifiés"])
        st.markdown(f"### Débouchés pour {selected_formation} :")
        for debouche in debouches:
            st.write(f"- {debouche}")

# Interaction LLM pour des recommandations supplémentaires
st.markdown("### Posez une question ou demandez une recommandation personnalisée :")
user_input = st.text_input("Votre question :", "")

if st.button("Envoyer"):
    if user_input.strip():
        with st.spinner("Chargement..."):
            try:
                # Ajouter le message utilisateur à l'historique
                message = f"Basé sur l'école {selected_ecole} et la formation {selected_formation}, {user_input}"
                st.session_state.messages.append(HumanMessage(content=message))

                # Générer une réponse
                llm.temperature = 0.7
                response = llm.invoke(st.session_state.messages)

                # Ajouter la réponse générée à l'historique
                st.session_state.messages.append(AIMessage(content=response.content))

                # Afficher la réponse
                st.success("Réponse générée !")
                st.write(response.content)
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
    else:
        st.warning("Veuillez entrer une question avant d'envoyer.")
