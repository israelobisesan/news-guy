import os
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from firebase import db

app = Flask(__name__)
CORS(app)

# Load NewsData API Key from environment
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY", "pub_6fa311d44ab545f289e80f78441c3d7c")

@app.route("/")
def home():
    return render_template("index.html")

# Fetch News
@app.route("/api/news", methods=["GET"])
def get_news():
    query = request.args.get("q", "technology")
    url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={query}&language=en"
    
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Like an article
@app.route("/api/like", methods=["POST"])
def like_article():
    data = request.get_json()
    article_id = data.get("article_id")

    if not article_id:
        return jsonify({"error": "Missing article_id"}), 400

    doc_ref = db.collection("likes").document(article_id)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.update({"count": doc.to_dict().get("count", 0) + 1})
    else:
        doc_ref.set({"count": 1})

    return jsonify({"message": "Liked successfully!"})

# Comment on an article
@app.route("/api/comment", methods=["POST"])
def comment_article():
    data = request.get_json()
    article_id = data.get("article_id")
    comment = data.get("comment")

    if not article_id or not comment:
        return jsonify({"error": "Missing article_id or comment"}), 400

    db.collection("comments").add({
        "article_id": article_id,
        "comment": comment
    })

    return jsonify({"message": "Comment added successfully!"})

if __name__ == "__main__":
    app.run(debug=True, port=5009)
