import itertools
import json
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

DATA_FILE = "notes.json"

def load_notes():
    with open(DATA_FILE, encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return []
    return json.loads(content)


def save_notes():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


notes = load_notes()
note_ids = itertools.count(max((n["id"] for n in notes), default=0) + 1)


def find_note(note_id):
    return next((n for n in notes if n["id"] == note_id), None)


@app.get("/")
def index():
    return "<h1>Гостевая книга</h1>"


@app.get("/notes")
def list_notes():
    author = request.args.get("author")

    sort = request.args.get("sort", "id")
    if sort not in ("id", "likes"):
        return jsonify(error="sort must be 'id' or 'likes'"), 400

    order = request.args.get("order", "asc")
    if order not in ("asc", "desc"):
        return jsonify(error="order must be 'asc' or 'desc'"), 400

    limit_raw = request.args.get("limit")
    if limit_raw is None:
        limit = 10
    else:
        try:
            limit = int(limit_raw)
        except (TypeError, ValueError):
            return jsonify(error="limit must be an integer"), 400
        if limit < 1 or limit > 100:
            return jsonify(error="limit must be between 1 and 100"), 400

    offset_raw = request.args.get("offset")
    if offset_raw is None:
        offset = 0
    else:
        try:
            offset = int(offset_raw)
        except (TypeError, ValueError):
            return jsonify(error="offset must be an integer"), 400
        if offset < 0:
            return jsonify(error="offset must be >= 0"), 400

    result = notes
    if author is not None:
        result = [n for n in result if n["author"] == author]

    result = sorted(result, key=lambda n: n[sort], reverse=(order == "desc"))

    return jsonify(result[offset:offset + limit])


@app.post("/notes")
def create_note():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    if not isinstance(data.get("author"), str) or not data["author"].strip():
        return jsonify(error="field 'author' (non-empty string) is required"), 400
    note = {
        "id": next(note_ids),
        "author": data["author"].strip(),
        "text": data["text"].strip(),
        "likes": 0,
    }
    notes.append(note)
    save_notes()
    return jsonify(note), 201


@app.get("/notes/<int:note_id>")
def get_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    return jsonify(note)


@app.put("/notes/<int:note_id>")
def replace_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    if not isinstance(data.get("author"), str) or not data["author"].strip():
        return jsonify(error="field 'author' (non-empty string) is required"), 400
    note["author"] = data["author"].strip()
    note["text"] = data["text"].strip()
    save_notes()
    return jsonify(note), 200


@app.patch("/notes/<int:note_id>")
def update_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    note["text"] = data["text"].strip()
    save_notes()
    return jsonify(note), 200


@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    notes.remove(note)
    save_notes()
    return "", 204


@app.delete("/notes")
def delete_notes_by_author():
    author = request.args.get("author")
    if not isinstance(author, str) or not author.strip():
        return jsonify(error="query parameter 'author' (non-empty string) is required"), 400
    author = author.strip()

    global notes
    to_delete = [n for n in notes if n["author"] == author]
    notes = [n for n in notes if n["author"] != author]
    save_notes()
    return jsonify(deleted=len(to_delete)), 200


@app.get("/authors")
def list_authors():
    stats = {}
    for n in notes:
        s = stats.setdefault(n["author"], {"author": n["author"], "notes": 0, "likes": 0})
        s["notes"] += 1
        s["likes"] += n.get("likes", 0)
    return jsonify(sorted(stats.values(), key=lambda x: x["author"]))


@app.post("/notes/<int:note_id>/like")
def like_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    note["likes"] += 1
    save_notes()
    return jsonify(note), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify(error="not found"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error="method not allowed"), 405


if __name__ == "__main__":
    app.run(debug=True)
