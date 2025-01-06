import streamlit as st
from chatbot_logic import initialize_chatbot, process_user_input

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
    st.session_state.messages.append({"role": "user", "content": f"Voici un contexte supplémentaire : {file_content}"})

# Champ d'entrée pour la question
user_input = st.text_input("Votre question :", "")

# Générer la réponse
if st.button("Envoyer"):
    if user_input.strip():
        with st.spinner("Chargement..."):
            try:
                response = process_user_input(
                    user_input=user_input,
                    language=language,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    messages=st.session_state.messages
                )
                st.session_state.messages.append({"role": "bot", "content": response})
                st.success("Réponse générée !")
                st.write(response)
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
    else:
        st.warning("Veuillez entrer une question avant d'envoyer.")

# Feedback sur la réponse
if st.session_state.messages:
    feedback = st.radio("La réponse vous a-t-elle aidé ?", ("Oui", "Non"))
    if feedback == "Non":
        st.text_input("Pourquoi ?", key="feedback_comment")
