# app.py - Cœur du serveur Python (Back-end)

from flask import Flask, request, jsonify, send_from_directory
import os

# Initialisation de l'application Flask
# Permet de servir les fichiers statiques (comme index.html) directement
app = Flask(__name__, static_folder='.', static_url_path='')

# 1. Route pour la page d'accueil (Sert le fichier index.html)
@app.route('/')
def index():
    # Envoie le fichier index.html à l'utilisateur
    return send_from_directory('.', 'index.html')

# 2. Route pour l'API de chat
@app.route('/api/chat', methods=['POST'])
def chat_api():
    # Récupère les données envoyées par le Front-end (message, prénom, email)
    data = request.json
    message = data.get('message', '')
    
    # --- ZONE DE LOGIQUE IA : C'EST ICI QUE VOUS DOIVREZ INSÉRER VOTRE VRAI CODE RAG/LLM ---
    
    # Ceci est la réponse simulée et les réponses codées en dur pour les boutons d'accueil
    if "guillaume peype" in message.lower():
        response_text = "Guillaume Peype est l'auteur de la note stratégique et poursuit un cursus Ingénieur par alternance à l'IMT Mines Alès."
    elif "aide" in message.lower() or "question" in message.lower():
        response_text = "Je suis prêt à vous répondre sur le contenu de la note stratégique RIBIÈRE."
    else:
        # Réponse par défaut en cas d'absence de logique IA connectée
        response_text = "Je n'ai pas pu accéder à ma logique d'IA. Le Back-end doit être restauré avec votre clé API et la logique RAG."

    # --- FIN DE LA ZONE DE LOGIQUE IA ---

    # Renvoie la réponse au Front-end en JSON
    return jsonify({"answer": response_text})

# 3. Route pour l'état du document (Simulé)
@app.route('/api/document-state')
def document_state():
    return jsonify({
        "content": "<h2>Contenu par défaut.</h2><p>Le contenu du document n'est pas disponible car la logique du Back-end a été perdue.</p>",
        "title": "Note Introuvable"
    })

# 4. Route pour l'upload de fichier (Simulé)
@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Cette fonction est vide, elle simule juste un succès pour que le Front-end ne plante pas
    return jsonify({"success": True, "textLength": 0, "message": "Upload simulé, pas de traitement réel."})


# Point d'entrée de l'application
if __name__ == '__main__':
    # Lance le serveur, utilisant le port défini par l'environnement (Render) ou 5000 par défaut
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))