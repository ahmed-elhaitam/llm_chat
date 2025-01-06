from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage

def initialize_chatbot():
    """Initialise le modèle ChatGroq."""
    return ChatGroq(
        model_name="llama-3.1-70b-versatile",
        groq_api_key="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",
        temperature=0
    )

def process_user_input(user_input, language, temperature, max_tokens, messages):
    """Gère l'entrée utilisateur et génère une réponse du chatbot."""
    chatbot = initialize_chatbot()
    chatbot.temperature = temperature
    chatbot.model_kwargs["max_tokens"] = max_tokens

    # Personnalisation du préfixe linguistique
    if language == "Français":
        prompt_prefix = "Répondez en français : "
    elif language == "Anglais":
        prompt_prefix = "Reply in English: "
    else:
        prompt_prefix = "Responda en español: "

    # Ajouter la question au contexte
    messages.append({"role": "user", "content": prompt_prefix + user_input})

    # Générer une réponse
    response = chatbot.invoke(messages)
    return response.content
