import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__, template_folder="../templates")

MONGO_URI = os.environ.get("MONGO_URI")

def get_db_collection():
    if not MONGO_URI:
        return None
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["dontpad_db"]
    return db["notes"]

@app.route("/", defaults={"subpath": ""}, methods=["GET", "POST"])
@app.route("/<path:subpath>", methods=["GET", "POST"])
def note_handler(subpath):
    try:
        notes_collection = get_db_collection()
        if notes_collection is None:
            return jsonify({"status": "error", "message": "MONGO_URI não configurada."}), 500

        path = request.args.get("path", subpath).strip("/")

        # Salvar nota (POST)
        if request.method == "POST":
            data = request.get_json() or {}
            content = data.get("content", "")
            notes_collection.update_one(
                {"path": path},
                {"$set": {"content": content}},
                upsert=True
            )
            return jsonify({"status": "success"})

        # Listar todas as sub-URLs existentes (GET ?action=list)
        if request.args.get("action") == "list":
            # Busca caminhos não vazios e ordena alfabeticamente
            cursor = notes_collection.find(
                {"path": {"$ne": ""}},
                {"_id": 0, "path": 1}
            ).sort("path", 1)
            paths = [doc["path"] for doc in cursor if doc.get("path")]
            return jsonify({"status": "success", "paths": paths})

        # Retornar JSON com o texto da nota (GET ?action=get)
        if request.args.get("action") == "get":
            note = notes_collection.find_one({"path": path})
            content = note.get("content", "") if note else ""
            return jsonify({"status": "success", "content": content})

        # Renderizar o HTML base
        return render_template("index.html")

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500