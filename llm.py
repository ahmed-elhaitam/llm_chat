import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from PyPDF2 import PdfReader

# Initialize LLM
llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    groq_api_key="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",
    temperature=0
)

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Page configuration
st.set_page_config(
    page_title="LLM Orientation Assistant",
    page_icon="🎓",
    layout="wide"
)

# Sidebar with advanced filtering options
st.sidebar.title("🔍 Filtrer les écoles")
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier PDF pour le contexte :", type=["pdf"])

if uploaded_file:
    # Read PDF content
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()

    # Display PDF content
    st.sidebar.markdown("### Contenu du fichier PDF :")
    st.sidebar.text_area("Contexte extrait du PDF", text, height=200)

# School data model with enriched information
school_data = pd.DataFrame([
        {"Nom": "École des sciences de l'information", "Sigle": "ESI", "Ville": "Rabat", "Spécialité": "Sciences de l'information", "Débouchés": "Data Analyst, Consultant en systèmes d'information"},
    {"Nom": "Académie internationale Mohammed VI de l'aviation civile", "Sigle": "AIAC", "Ville": "Casablanca", "Spécialité": "Métiers de l'aviation", "Débouchés": "Pilote, Contrôleur aérien"},
    {"Nom": "École Hassania des travaux publics", "Sigle": "EHTP", "Ville": "Casablanca", "Spécialité": "Polyvalente", "Débouchés": "Ingénieur Civil, Manager de projet"},
    {"Nom": "École Mohammadia d'ingénieurs", "Sigle": "EMI", "Ville": "Rabat", "Spécialité": "Polyvalente", "Débouchés": "Ingénieur Mécanique, Consultant technique"},
    {"Nom": "École nationale d'industrie minérale", "Sigle": "ENIM", "Ville": "Rabat", "Spécialité": "Polyvalente", "Débouchés": "Ingénieur Minier, Consultant en Géotechnique"},
    {"Nom": "Écoles nationales des sciences appliquées", "Sigle": "ENSA", "Ville": "11 villes", "Spécialité": "Polyvalente", "Débouchés": "Développeur logiciel, Ingénieur électronique"},
    {"Nom": "École nationale supérieure d'arts et métiers", "Sigle": "ENSAM", "Ville": "Meknès, Casablanca", "Spécialité": "Polyvalente", "Débouchés": "Ingénieur en Production, Responsable de Maintenance"},
    {"Nom": "École nationale supérieure d'électricité et de mécanique de Casablanca", "Sigle": "ENSEM", "Ville": "Casablanca", "Spécialité": "Ingénieurs électro-mécaniciens, Génie informatique", "Débouchés": "Ingénieur Électrique, Développeur Systèmes embarqués"},
    {"Nom": "École nationale supérieure d'informatique et d'analyse des systèmes", "Sigle": "ENSIAS", "Ville": "Rabat", "Spécialité": "Métiers de l'informatique", "Débouchés": "Développeur logiciel, Expert en sécurité informatique"},
    {"Nom": "École supérieure des industries du textile et de l'habillement", "Sigle": "ESITH", "Ville": "Casablanca", "Spécialité": "Génie industriel", "Débouchés": "Ingénieur Logistique, Responsable de production"},
    {"Nom": "Institut agronomique et vétérinaire Hassan II", "Sigle": "IAV", "Ville": "Rabat", "Spécialité": "Agronomie, topographie", "Débouchés": "Agronome, Spécialiste en gestion des ressources naturelles"},
    {"Nom": "Institut national des postes et télécommunications", "Sigle": "INPT", "Ville": "Rabat", "Spécialité": "Métiers des télécoms et des technologies d'information et de communication", "Débouchés": "Ingénieur Télécoms, Administrateur Réseaux"},
    {"Nom": "Institut national de statistique et d'économie appliquée", "Sigle": "INSEA", "Ville": "Rabat", "Spécialité": "Métiers de l'informatique, de l'économie, statistique et finance", "Débouchés": "Data Scientist, Analyste financier"},
    {"Nom": "Cycle Ingénieur des facultés des sciences et techniques", "Sigle": "FST", "Ville": "5 villes", "Spécialité": "Polyvalente", "Débouchés": "Ingénieur dans divers secteurs, Consultant IT"},
    {"Nom": "Ecole Normale Supérieure de l'Enseignement Technique", "Sigle": "ENSET", "Ville": "Mohammedia, Rabat", "Spécialité": "Polyvalente", "Débouchés": "Formateur technique, Responsable Pédagogique"},
    {"Nom": "École Supérieure des Sciences et Technologies de l'Ingénierie", "Sigle": "ESSTI", "Ville": "Rabat", "Spécialité": "Polyvalente", "Débouchés": "Ingénieur en développement, Consultant industriel"},
    {"Nom": "École Centrale Casablanca", "Sigle": "ECC", "Ville": "Casablanca", "Spécialité": "Généraliste", "Débouchés": "Ingénieur généraliste, Chef de projet"}
])

# Display data
st.title("🎓 Assistant d'Orientation - LLM")
st.markdown("**Explorez les écoles, découvrez les formations, et obtenez des réponses adaptées avec un chatbot IA.**")

# School selection and details
selected_school = st.selectbox("Choisissez une école :", school_data["Nom"])
school_info = school_data[school_data["Nom"] == selected_school].iloc[0]

# Display school details
st.subheader("📍 Informations sur l'école")
st.markdown(f"**Nom :** {school_info['Nom']}")
st.markdown(f"**Ville :** {school_info['Ville']}")
st.markdown(f"**Spécialité :** {school_info['Spécialité']}")

st.subheader("🎯 Débouchés")
st.markdown(f"**Débouchés :** {school_info['Débouchés']}")

# Interaction with LLM
st.markdown("### 💬 Posez une question :")
user_input = st.text_input("Votre question :", "")

if st.button("Envoyer"):
    if user_input.strip():
        with st.spinner("Chargement..."):
            try:
                # Combine question with school context
                message = f"L'utilisateur a sélectionné l'école {school_info['Nom']} ({school_info['Ville']}). Question : {user_input}"
                st.session_state["messages"].append(HumanMessage(content=message))

                # Generate LLM response
                response = llm.invoke(st.session_state["messages"])

                # Add response to conversation history
                st.session_state["messages"].append(AIMessage(content=response.content))

                # Display response
                st.success("Réponse générée 🎉")
                st.markdown(f"**🤖 LLM :** {response.content}")
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
    else:
        st.warning("Veuillez entrer une question avant d'envoyer.")
