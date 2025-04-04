import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask("wingX", template_folder="templates")

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/getAnswer", methods=["POST"])
def get_answer():
    data = request.get_json()
    question = data.get("question", "").strip()
    
    if not question:
        return jsonify({"answer": "Please enter a valid question."}), 400
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-3.5-turbo",  # Adjust the model as needed
        "messages": [{"role": "user", "content": question}]
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response_data = response.json()
        
        if "choices" in response_data and response_data["choices"]:
            answer = response_data["choices"][0]["message"]["content"]
        else:
            answer = "Could not fetch an answer. Try again."
        
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": "Error connecting to API."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
