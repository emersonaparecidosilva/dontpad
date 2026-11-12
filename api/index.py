import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__, template_folder="../templates")
print('Teste')

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
            return jsonify({
                "status": "error", 
                "message": "MONGO_URI não configurada nas variáveis da Vercel."
            }), 500

        # Captura o caminho real enviado pelo rewrite do vercel.json
        path = request.args.get("path", subpath).strip("/")

        # POST: Salva ou atualiza a nota específica daquele path
        if request.method == "POST":
            data = request.get_json() or {}
            content = data.get("content", "")
            
            notes_collection.update_one(
                {"path": path},
                {"$set": {"content": content}},
                upsert=True
            )
            return jsonify({"status": "success", "path": path})

        # GET: Busca o conteúdo exclusivo daquele path
        content = ""
        note = notes_collection.find_one({"path": path})
        if note:
            content = note.get("content", "")

        return render_template("index.html", path=path, content=content)

    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Erro na conexão com MongoDB: {str(e)}"
        }), 500