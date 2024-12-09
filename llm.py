import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage

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
domains = st.sidebar.multiselect(
    "Domaines d'études",
    ["Polyvalente", "Informatique", "Ingénieurs", "Télécommunications", "Agronomie"],
    default=[]
)
location = st.sidebar.selectbox(
    "Localisation",
    ["Toutes", "Casablanca", "Rabat", "11 villes", "5 villes", "Mohammedia"],
    index=0
)

# School data model with enriched information
school_data = pd.DataFrame( [
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

# Apply filters
filtered_schools = school_data.copy()
if domains:
    filtered_schools = filtered_schools[filtered_schools["Domaines"].isin(domains)]
if location != "Toutes":
    filtered_schools = filtered_schools[filtered_schools["Ville"] == location]

# Display data
st.title("🎓 Assistant d'Orientation - LLM")
st.markdown("**Explorez les écoles, découvrez les formations, et obtenez des réponses adaptées avec un chatbot IA.**")

# Pie chart visualization
st.sidebar.markdown("### 📊 Répartition des Écoles")
fig = px.pie(school_data, names="Ville", title="Répartition des écoles par localisation")
st.sidebar.plotly_chart(fig, use_container_width=True)

# Two-column layout for school details
col1, col2 = st.columns(2)

# School selection and details
selected_school = st.selectbox("Choisissez une école :", filtered_schools["Nom"])
school_info = school_data[school_data["Nom"] == selected_school].iloc[0]

# Display school details
with col1:
    st.subheader("📍 Informations sur l'école")
    st.markdown(f"**Nom :** {school_info['Nom']}")
    st.markdown(f"**Ville :** {school_info['Ville']}")
    st.markdown(f"**Domaines :** {school_info['Domaines']}")

with col2:
    st.subheader("🎯 Débouchés")
    st.markdown(f"**Débouchés :** {school_info['Débouchés']}")

# Interaction with LLM
st.markdown("### 💬 Posez une question :")
user_input = st.text_input("Votre question :", "")

if st.button("Envoyer"):
    if user_input.strip():
        with st.spinner("Chargement..."):
            try:
                # Dynamic temperature adjustment
                query_complexity = len(user_input.split())
                llm.temperature = 0.5 if query_complexity < 10 else 0.7

                # Add user query to conversation history
                st.session_state["messages"].append(HumanMessage(content=user_input))

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
