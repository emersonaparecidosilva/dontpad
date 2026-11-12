import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder="../templates")

MONGO_URI = os.environ.get("MONGO_URI")

def get_db_collection():
    if not MONGO_URI:
        return None
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["dontpad_db"]
    return db["notes"]

def is_authorized(note, provided_password):
    if not note or not note.get("password_hash"):
        return True
    if not provided_password:
        return False
    return check_password_hash(note["password_hash"], provided_password)

@app.route("/", defaults={"subpath": ""}, methods=["GET", "POST", "DELETE"])
@app.route("/<path:subpath>", methods=["GET", "POST", "DELETE"])
def note_handler(subpath):
    try:
        notes_collection = get_db_collection()
        if notes_collection is None:
            return jsonify({"status": "error", "message": "MONGO_URI não configurada."}), 500

        path = request.args.get("path", subpath).strip("/")
        provided_password = request.headers.get("X-Note-Password", "")
        action = request.args.get("action")

        # 1. Listar todas as sub-URLs existentes (indica quais têm cadeado)
        if action == "list":
            cursor = notes_collection.find(
                {"path": {"$nin": ["", "api/index"]}},
                {"_id": 0, "path": 1, "password_hash": 1}
            ).sort("path", 1)
            items = [
                {"path": doc["path"], "locked": bool(doc.get("password_hash"))}
                for doc in cursor if doc.get("path")
            ]
            return jsonify({"status": "success", "items": items})

        # 2. Definir ou remover senha da nota atual
        if action == "set_password" and request.method == "POST":
            if path == "api/index":
                return jsonify({"status": "ignored"})
            
            note = notes_collection.find_one({"path": path})
            if not is_authorized(note, provided_password):
                return jsonify({"status": "locked", "message": "Senha atual incorreta."}), 403

            data = request.get_json() or {}
            new_password = data.get("new_password", "").strip()

            if new_password:
                pwd_hash = generate_password_hash(new_password)
                notes_collection.update_one(
                    {"path": path},
                    {"$set": {"password_hash": pwd_hash}, "$setOnInsert": {"content": ""}},
                    upsert=True
                )
                return jsonify({"status": "success", "locked": True})
            else:
                notes_collection.update_one(
                    {"path": path},
                    {"$unset": {"password_hash": ""}}
                )
                return jsonify({"status": "success", "locked": False})

        # 3. Excluir uma nota
        if request.method == "DELETE" or action == "delete":
            if path and path != "api/index":
                note = notes_collection.find_one({"path": path})
                if not is_authorized(note, provided_password):
                    return jsonify({"status": "locked", "message": "Senha necessária para excluir."}), 403
                notes_collection.delete_one({"path": path})
            return jsonify({"status": "success"})

        # 4. Salvar texto da nota (POST)
        if request.method == "POST":
            if path == "api/index":
                return jsonify({"status": "ignored"})
            
            note = notes_collection.find_one({"path": path})
            if not is_authorized(note, provided_password):
                return jsonify({"status": "locked", "message": "Nota protegida por senha."}), 403

            data = request.get_json() or {}
            content = data.get("content", "")
            notes_collection.update_one(
                {"path": path},
                {"$set": {"content": content}},
                upsert=True
            )
            return jsonify({"status": "success"})

        # 5. Retornar conteúdo da nota (GET ?action=get)
        if action == "get":
            note = notes_collection.find_one({"path": path})
            if not is_authorized(note, provided_password):
                return jsonify({"status": "locked", "locked": True})

            content = note.get("content", "") if note else ""
            locked = bool(note.get("password_hash")) if note else False
            return jsonify({"status": "success", "content": content, "locked": locked})

        # 6. Renderizar o HTML base
        return render_template("index.html")

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500