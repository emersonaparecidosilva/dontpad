import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__, template_folder="../templates")

# Conexão com o MongoDB Atlas via variável de ambiente da Vercel
MONGO_URI = os.environ.get("MONGO_URI")

client = None
if MONGO_URI:
    client = MongoClient(MONGO_URI)
    db = client["dontpad_db"]
    notes_collection = db["notes"]

@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def note_handler(path):
    if client is None:
        return jsonify({
            "status": "error",
            "message": "MONGO_URI não configurada nas variáveis de ambiente."
        }), 500

    # Atualiza ou insere a nota no MongoDB Atlas
    if request.method == "POST":
        data = request.get_json() or {}
        content = data.get("content", "")
        
        notes_collection.update_one(
            {"path": path},
            {"$set": {"content": content}},
            upsert=True
        )
        return jsonify({"status": "success"})

    # Busca o conteúdo da nota no MongoDB Atlas
    content = ""
    note = notes_collection.find_one({"path": path})
    if note:
        content = note.get("content", "")

    return render_template("index.html", path=path, content=content)