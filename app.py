# app.py - Version 2.0 avec Gemini API et RAG Simulé

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests # Pour lire le contenu du PDF s'il était en ligne
from io import BytesIO

# Importation spécifique pour Gemini
try:
    from google import genai
except ImportError:
    # Ce bloc sera exécuté si la librairie 'google-genai' n'est pas installée
    # (cela sera réglé par le fichier requirements.txt lors du déploiement)
    pass

# Initialisation de l'application Flask
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app) # Active CORS pour que l'interface puisse parler au serveur

# --- Variable Globale pour stocker le contenu du document ---
# Dans une application réelle, ceci serait une base de données vectorielle (index)
document_content = "Le document n'est pas encore indexé ou est introuvable."
document_title = "Note Stratégique RIBIÈRE"
document_author = "Guillaume Peype"


# 1. Route pour la page d'accueil (Sert le fichier index.html)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


# 2. Route pour l'API de chat (LOGIQUE D'IA)
@app.route('/api/chat', methods=['POST'])
def chat_api():
    global document_content

    # Vérification de la clé API
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_key:
        return jsonify({"answer": "Erreur: La clé GEMINI_API_KEY n'est pas configurée sur Vercel."}), 500

    try:
        data = request.json
        user_message = data.get('message', 'Bonjour')

        # 1. Préparation du Prompt (Simule le RAG : nous ajoutons le contenu au prompt)
        # Note : Dans une vraie application RAG, nous n'enverrions que les extraits pertinents.
        full_prompt = (
            f"Tu es un assistant documentaire intelligent spécialisé dans la note stratégique RIBIÈRE. "
            f"Le contenu du document est : «{document_content}». "
            f"Réponds précisément à la question de l'utilisateur en te basant uniquement sur ce document et tes connaissances. "
            f"Question de l'utilisateur : {user_message}"
        )

        # 2. Appel à l'API Gemini
        client = genai.Client(api_key=gemini_key)
        
        # Nous utilisons le modèle le plus adapté à la rapidité et au texte
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        return jsonify({"answer": response.text})

    except Exception as e:
        # En cas d'erreur lors de l'appel à l'API (clé invalide, erreur réseau, etc.)
        print(f"Erreur lors de l'appel à Gemini : {e}")
        return jsonify({"answer": f"Une erreur est survenue lors de l'appel au service : {str(e)}. Vérifiez la connexion au serveur RAG."}), 500


# 3. Route pour l'état du document
@app.route('/api/document-state')
def document_state():
    global document_title, document_author
    
    # Le contenu ici est simulé pour l'affichage de l'auteur et du titre sur l'interface
    return jsonify({
        "content": f"<h2>{document_title}</h2><p>Rédigée par {document_author} pour RIBIÈRE.</p><p>Le document est prêt à être interrogé.</p>",
        "title": document_title
    })

# 4. Route pour l'upload de fichier (SIMULATION AVANCÉE)
@app.route('/api/upload', methods=['POST'])
def upload_file():
    global document_content, document_title
    
    if 'document' not in request.files:
        return jsonify({"success": False, "message": "Aucun fichier n'a été envoyé."}), 400
    
    file = request.files['document']
    
    # ⚠️ Ceci est une simulation : l'upload de PDF réel nécessite des outils lourds
    if file.filename.endswith('.pdf'):
        # Nous simulons que le PDF a été traité et que son contenu est stocké.
        document_content = f"CONTENU DU DOCUMENT CHARGÉ : {file.filename}. Le système RAG a réussi à le charger, mais le texte n'a pas été extrait dans cette version simple. L'assistant répondra en utilisant son 'contexte' global."
        document_title = file.filename
        
        return jsonify({"success": True, "textLength": 100, "message": f"Fichier '{file.filename}' chargé et prêt à être interrogé."})
    
    return jsonify({"success": False, "message": "Format de fichier non supporté."}), 400


# Point d'entrée de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
