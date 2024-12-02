import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage

# Initialiser le modèle ChatGroq
llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    groq_api_key="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",
    temperature=0
)

# Interface utilisateur Streamlit
st.title("Chatbot Amélioré")
st.markdown("Posez une question et continuez la conversation !")

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.markdown(f"**Vous :** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.markdown(f"**Bot :** {msg.content}")

# Champ d'entrée pour la question
user_input = st.text_input("Votre question :", "")

# Générer la réponse lorsque l'utilisateur clique sur le bouton
if st.button("Envoyer"):
    if user_input.strip():
        with st.spinner("Chargement..."):
            try:
                # Ajouter le message utilisateur à l'historique
                st.session_state.messages.append(HumanMessage(content=user_input))

                # Générer une réponse basée sur l'historique
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
