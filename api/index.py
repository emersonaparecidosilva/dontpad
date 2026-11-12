import os
from urllib.parse import unquote
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

def get_real_path(subpath):
    # 1. Prioriza o parâmetro ?path= enviado explicitamente
    if "path" in request.args:
        return unquote(request.args.get("path", "")).strip("/")
    
    # 2. Lê os cabeçalhos internos da Vercel que guardam a URL original
    for header in ["x-vercel-original-path", "x-invoke-path", "x-matched-path"]:
        val = request.headers.get(header)
        if val and not val.startswith("/api/"):
            return unquote(val.split("?")[0]).strip("/")
            
    return unquote(subpath).strip("/")

@app.route("/", defaults={"subpath": ""}, methods=["GET", "POST"])
@app.route("/<path:subpath>", methods=["GET", "POST"])
def note_handler(subpath):
    try:
        notes_collection = get_db_collection()
        if notes_collection is None:
            return jsonify({
                "status": "error", 
                "message": "MONGO_URI não configurada."
            }), 500

        path = get_real_path(subpath)

        # POST: Salva ou atualiza a nota daquele caminho
        if request.method == "POST":
            data = request.get_json() or {}
            content = data.get("content", "")
            
            notes_collection.update_one(
                {"path": path},
                {"$set": {"content": content}},
                upsert=True
            )
            return jsonify({"status": "success", "path": path})

        # GET: Busca o conteúdo da nota
        content = ""
        note = notes_collection.find_one({"path": path})
        if note:
            content = note.get("content", "")

        return render_template("index.html", path=path, content=content)

    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Erro: {str(e)}"
        }), 500