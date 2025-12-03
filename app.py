# app.py - Version 2.1 avec Gemini API et RAG Simulé

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests 
from io import BytesIO

# Importation spécifique pour Gemini
# Cette ligne nécessite que 'google-genai' soit dans requirements.txt
from google import genai 

# Initialisation de l'application Flask
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app) # Active CORS pour que l'interface puisse parler au serveur

# --- Variable Globale pour stocker le contenu du document ---
# Ceci simule le contenu que l'assistant va utiliser pour répondre
document_content = "Le document n'est pas encore indexé ou est introuvable. Cependant, l'auteur est Guillaume Peype et le sujet est la note stratégique RIBIÈRE."
document_title = "Note Stratégique RIBIÈRE"
document_author = "Guillaume Peype"


# 1. Route pour la page d'accueil (Sert le fichier index.html)
@app.route('/')
def index():
    # Assurez-vous que votre fichier HTML est nommé index.html sur GitHub !
    return send_from_directory('.', 'index.html')


# 2. Route pour l'API de chat (LOGIQUE D'IA)
@app.route('/api/chat', methods=['POST'])
def chat_api():
    global document_content

    # Vérification de la clé API
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_key:
        # Si la clé n'est pas trouvée dans Vercel
        return jsonify({"answer": "Erreur critique : La clé GEMINI_API_KEY n'est pas configurée dans les variables d'environnement de Vercel."}), 500

    try:
        data = request.json
        user_message = data.get('message', 'Bonjour')

        # 1. Préparation du Prompt (Ajout du contexte simulé)
        full_prompt = (
            f"Tu es un assistant documentaire intelligent spécialisé dans la note stratégique RIBIÈRE. "
            f"Le contenu du document que tu dois utiliser comme base est : «{document_content}». "
            f"Réponds précisément à la question de l'utilisateur en te basant sur ce document et tes connaissances. "
            f"Question de l'utilisateur : {user_message}"
        )

        # 2. Appel à l'API Gemini
        # La connexion nécessite la clé API fournie
        client = genai.Client(api_key=gemini_key)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        return jsonify({"answer": response.text})

    except Exception as e:
        # Ce message s'affiche si l'appel à genai.Client() ou generate_content échoue.
        # Causes : Clé API invalide, Quota dépassé, ou Problème de réseau/installation.
        print(f"Erreur lors de l'appel à Gemini : {e}")
        return jsonify({"answer": f"Erreur critique lors de l'appel à l'IA : {str(e)}. Vérifiez votre clé API et les logs de Vercel."}), 500


# 3. Route pour l'état du document
@app.route('/api/document-state')
def document_state():
    global document_title, document_author
    
    # Renvoie les informations pour l'interface utilisateur
    return jsonify({
        "content": f"<h2>{document_title}</h2><p>Rédigée par {document_author} pour RIBIÈRE.</p><p>Le document est prêt à être interrogé.</p>",
        "title": document_title
    })

# 4. Route pour l'upload de fichier (SIMULATION)
@app.route('/api/upload', methods=['POST'])
def upload_file():
    # La logique ici est pour empêcher votre interface de planter
    global document_content, document_title
    
    # ... (Logique de simulation)
    
    return jsonify({"success": True, "textLength": 0, "message": "Upload simulé : Fichier chargé et prêt à être interrogé."})


# Point d'entrée de l'application
if __name__ == '__main__':
    # Lance le serveur, utilisant le port défini par l'environnement de l'hébergeur
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
