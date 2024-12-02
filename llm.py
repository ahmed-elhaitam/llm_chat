import streamlit as st
from langchain_groq import ChatGroq

# Initialiser le modèle ChatGroq
llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",  # Remplacez par le nom de votre modèle
    groq_api_key="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",  # Clé API
    temperature=0  # Ajustez la température selon vos besoins
)

# Interface utilisateur Streamlit
st.title("Chat avec LangChain et ChatGroq")
st.markdown("Posez une question et obtenez une réponse !")

# Champ d'entrée pour la question
user_input = st.text_input("Votre question :", "")

# Afficher la réponse lorsque l'utilisateur soumet une question
if st.button("Envoyer"):
    if user_input.strip():  # Vérifiez si l'entrée n'est pas vide
        with st.spinner("Chargement..."):
            try:
                # Appeler le modèle pour générer une réponse
                response = llm.invoke([{"role": "user", "content": user_input}])
                st.success("Réponse générée !")
                st.write(response['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
    else:
        st.warning("Veuillez entrer une question avant d'envoyer.")
