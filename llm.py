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
st.markdown("**Sélectionnez une école et découvrez ses débouchés avec un LLM !**")

# Données des écoles
ecoles = [
    {"Nom": "Académie internationale Mohammed VI de l'aviation civile", "Sigle": "AIAC", "Ville": "Casablanca", "Spécialité": "Polyvalente et Métiers de l'aviation"},
    {"Nom": "École Hassania des travaux publics", "Sigle": "EHTP", "Ville": "Casablanca", "Spécialité": "Polyvalente"},
    {"Nom": "École Mohammadia d'ingénieurs", "Sigle": "EMI", "Ville": "Rabat", "Spécialité": "Polyvalente"},
    {"Nom": "École nationale d'industrie minérale", "Sigle": "ENIM", "Ville": "Rabat", "Spécialité": "Polyvalente"},
    {"Nom": "Écoles nationales des sciences appliquées", "Sigle": "ENSA", "Ville": "11 villes", "Spécialité": "Polyvalente"},
    {"Nom": "École nationale supérieure d'arts et métiers", "Sigle": "ENSAM", "Ville": "Meknès, Casablanca", "Spécialité": "Polyvalente"},
    {"Nom": "École nationale supérieure d'électricité et de mécanique de Casablanca", "Sigle": "ENSEM", "Ville": "Casablanca", "Spécialité": "Ingénieurs électro-mécaniciens, Génie informatique"},
    {"Nom": "École nationale supérieure d'informatique et d'analyse des systèmes", "Sigle": "ENSIAS", "Ville": "Rabat", "Spécialité": "Métiers de l'informatique"},
    {"Nom": "École supérieure des industries du textile et de l'habillement", "Sigle": "ESITH", "Ville": "Casablanca", "Spécialité": "Génie industriel"},
    {"Nom": "Institut agronomique et vétérinaire Hassan II", "Sigle": "IAV", "Ville": "Rabat", "Spécialité": "Agronomie, topographie"},
    {"Nom": "Institut national des postes et télécommunications", "Sigle": "INPT", "Ville": "Rabat", "Spécialité": "Métiers des télécoms et des technologies d'information et de communication"},
    {"Nom": "Institut national de statistique et d'économie appliquée", "Sigle": "INSEA", "Ville": "Rabat", "Spécialité": "Métiers de l'informatique, de l'économie, statistique et finance"},
    {"Nom": "Cycle Ingénieur des facultés des sciences et techniques", "Sigle": "FST", "Ville": "5 villes", "Spécialité": "Polyvalente"},
    {"Nom": "École des sciences de l'information", "Sigle": "ESI", "Ville": "Rabat", "Spécialité": "Sciences de l'information"},
    {"Nom": "Ecole Normale Supérieure de l'Enseignement Technique", "Sigle": "ENSET", "Ville": "Mohammedia, Rabat", "Spécialité": "Polyvalente"},
    {"Nom": "École Supérieure des Sciences et Technologies de l'Ingénierie", "Sigle": "ESSTI", "Ville": "Rabat", "Spécialité": "Polyvalente"},
    {"Nom": "École Centrale Casablanca", "Sigle": "ECC", "Ville": "Casablanca", "Spécialité": "Généraliste"},
]

# Liste des écoles
ecoles_nom = [ecole["Nom"] for ecole in ecoles]
selected_ecole = st.selectbox("Choisissez une école :", ecoles_nom)

# Afficher les détails de l'école sélectionnée
if selected_ecole:
    ecole_info = next(ecole for ecole in ecoles if ecole["Nom"] == selected_ecole)
    st.markdown(f"**Nom** : {ecole_info['Nom']}")
    st.markdown(f"**Sigle** : {ecole_info['Sigle']}")
    st.markdown(f"**Ville(s)** : {ecole_info['Ville']}")
    st.markdown(f"**Spécialité** : {ecole_info['Spécialité']}")

# Interaction LLM pour des débouchés ou recommandations
st.markdown("### Posez une question au LLM :")
user_input = st.text_input("Votre question :", "")

if st.button("Envoyer"):
    if user_input.strip():
        with st.spinner("Chargement..."):
            try:
                # Ajouter le contexte de l'école à la question
                message = f"École sélectionnée : {selected_ecole}. {user_input}"
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
