from flask import Flask, request, jsonify
import requests
from io import BytesIO
import docx

app = Flask(__name__)

@app.route("/extract-docx-text", methods=["POST"])
def extract_docx_text():
    data = request.json
    doc_url = data.get("doc_url")

    if not doc_url:
        return jsonify({"error": "Missing 'doc_url' field"}), 400

    try:
        # Download the .docx file
        response = requests.get(doc_url)
        response.raise_for_status()

        # Extract text from .docx using python-docx
        document = docx.Document(BytesIO(response.content))
        text = "\n".join([para.text for para in document.paragraphs])

        return jsonify({"text": text.strip()})

    except Exception as e:
        print("🚨 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

