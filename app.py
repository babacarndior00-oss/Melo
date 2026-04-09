import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# --- 1. CONFIGURATION ET CONNEXION ---
# On charge les variables cachées dans le fichier .env
load_dotenv()

# On configure le client pour qu'il pointe vers les serveurs gratuits de Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# --- 2. INTERFACE GRAPHIQUE ---
st.set_page_config(page_title="Chatbot Scolaire", page_icon="🤖")
st.title("🤖 Mon Assistant IA (Version Groq)")

# --- 3. GESTION DE LA MÉMOIRE ---
# On crée une "boîte" dans la mémoire de Streamlit pour stocker l'historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# On réaffiche tous les anciens messages à chaque fois que la page se rafraîchit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. MOTEUR DU CHATBOT ---
# Cette ligne crée la barre de texte en bas de l'écran et attend que l'utilisateur tape quelque chose
if prompt := st.chat_input("Posez votre question ici..."):
    
    # Étape A : On sauvegarde et on affiche le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Étape B : On interroge l'IA (LLaMA 3) avec tout l'historique
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Nouveau modèle ultra-performant
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=False,
        )
        # On extrait le texte de la réponse envoyée par l'IA
        response = stream.choices[0].message.content
        st.markdown(response)
    
    # Étape C : On sauvegarde la réponse de l'IA dans l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})