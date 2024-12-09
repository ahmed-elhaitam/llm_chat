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
specialites = st.sidebar.multiselect(
    "Spécialités d'études",
    [
        "Polyvalente", "Informatique", "Ingénieurs",
        "Télécommunications", "Agronomie", "Généraliste", "Métiers de l'aviation",
    ],
    default=[]
)
location = st.sidebar.selectbox(
    "Localisation",
    ["Toutes", "Casablanca", "Rabat", "11 villes", "5 villes", "Mohammedia", "Meknès"],
    index=0
)

# Enriched school data model
school_data = pd.DataFrame([
    {"Nom": "Académie internationale Mohammed VI de l'aviation civile", "Sigle": "AIAC", "Ville": "Casablanca", "Spécialité": "Métiers de l'aviation", "Formations": ["Pilotage", "Gestion aérienne"], "Débouchés": "Pilote, Contrôleur aérien"},
    {"Nom": "École Hassania des travaux publics", "Sigle": "EHTP", "Ville": "Casablanca", "Spécialité": "Polyvalente", "Formations": ["Génie Civil", "Hydraulique"], "Débouchés": "Ingénieur Civil, Manager de projet"},
    {"Nom": "École Mohammadia d'ingénieurs", "Sigle": "EMI", "Ville": "Rabat", "Spécialité": "Polyvalente", "Formations": ["Génie Informatique", "Génie Mécanique"], "Débouchés": "Ingénieur Mécanique, Consultant technique"},
    {"Nom": "Écoles nationales des sciences appliquées", "Sigle": "ENSA", "Ville": "11 villes", "Spécialité": "Polyvalente", "Formations": ["Développement logiciel", "Réseaux"], "Débouchés": "Développeur logiciel, Ingénieur électronique"},
    {"Nom": "Institut national des postes et télécommunications", "Sigle": "INPT", "Ville": "Rabat", "Spécialité": "Télécommunications", "Formations": ["Ingénierie Télécoms"], "Débouchés": "Ingénieur Télécoms, Administrateur Réseaux"},
    {"Nom": "Institut national de statistique et d'économie appliquée", "Sigle": "INSEA", "Ville": "Rabat", "Spécialité": "Statistiques", "Formations": ["Data Science", "Analyse Financière"], "Débouchés": "Data Scientist, Analyste financier"},
    {"Nom": "École nationale supérieure d'informatique et d'analyse des systèmes", "Sigle": "ENSIAS", "Ville": "Rabat", "Spécialité": "Informatique", "Formations": ["Intelligence Artificielle", "Cybersécurité"], "Débouchés": "Développeur logiciel, Expert en cybersécurité"},
])

# Apply filters
filtered_schools = school_data.copy()
if specialites:
    filtered_schools = filtered_schools[filtered_schools["Spécialité"].str.contains("|".join(specialites), case=False)]
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
if not filtered_schools.empty:
    selected_school = st.selectbox("Choisissez une école :", filtered_schools["Nom"])
    school_info = filtered_schools[filtered_schools["Nom"] == selected_school].iloc[0]

    # Display school details
    with col1:
        st.subheader("📍 Informations sur l'école")
        st.markdown(f"**Nom :** {school_info['Nom']}")
        st.markdown(f"**Ville :** {school_info['Ville']}")
        st.markdown(f"**Spécialité :** {school_info['Spécialité']}")

    with col2:
        st.subheader("🎓 Formations disponibles")
        formations = school_info["Formations"]
        for formation in formations:
            st.markdown(f"- {formation}")

        st.subheader("🎯 Débouchés")
        st.markdown(f"**Débouchés :** {school_info['Débouchés']}")
else:
    st.warning("Aucune école correspondante aux critères sélectionnés.")

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
