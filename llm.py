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
])

# Display data
st.title("🎓 Assistant d'Orientation - LLM")
st.markdown("**Explorez les écoles et obtenez des réponses adaptées avec un chatbot IA.**")

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
