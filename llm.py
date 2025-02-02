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
st.title("Chatbot Intelligent avec LangChain et ChatGroq")
st.markdown("Posez une question, ajoutez des fichiers pour le contexte et personnalisez les paramètres !")

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Barre latérale pour les paramètres
st.sidebar.title("Paramètres du modèle")
temperature = st.sidebar.slider("Température :", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.number_input("Nombre maximum de tokens :", 10, 1000, 256)
language = st.sidebar.selectbox("Langue :", ["Français", "Anglais", "Espagnol"])

# Télécharger un fichier pour le contexte
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier pour le contexte :", type=["pdf", "txt", "csv"])
if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    st.session_state.messages.append(HumanMessage(content=f"Voici un contexte supplémentaire : {file_content}"))

# Personnalisation des messages en fonction de la langue
if language == "Français":
    prompt_prefix = "Répondez en français : "
elif language == "Anglais":
    prompt_prefix = "Reply in English: "
else:
    prompt_prefix = "Responda en español: "

# Afficher l'historique des conversations
for msg in st.session_state.messages:
    with st.container():
        if isinstance(msg, HumanMessage):
            st.markdown(f"🧑‍💻 Vous :** {msg.content}", unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f"🤖 Bot :** {msg.content}", unsafe_allow_html=True)

# Champ d'entrée pour la question
user_input = st.text_input("Votre question :", "")

# Générer la réponse
if st.button("Envoyer"):
    if user_input.strip():
        with st.spinner("Chargement..."):
            try:
                # Ajouter le message utilisateur à l'historique
                st.session_state.messages.append(HumanMessage(content=prompt_prefix + user_input))

                # Générer une réponse
                llm.temperature = temperature
                llm.model_kwargs["max_tokens"] = max_tokens
                response = llm.invoke(st.session_state.messages)

                # Ajouter la réponse du bot à l'historique
                st.session_state.messages.append(AIMessage(content=response.content))

                # Afficher la réponse
                st.success("Réponse générée !")
                st.write(response.content)
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
    else:
        st.warning("Veuillez entrer une question avant d'envoyer.")

# Feedback sur la réponse
if st.session_state.messages:
    feedback = st.radio("La réponse vous a-t-elle aidé ?", ("Oui", "Non"))
    if feedback == "Non":
        st.text_input("Pourquoi ?", key="feedback_comment")
