from flask import Flask, jsonify
from flask_cors import CORS
from gmail_handler import fetch_gmail_messages  

app = Flask(__name__)
CORS(app)  

@app.route("/fetch/gmail", methods=["GET"])
def fetch_emails():
    emails = fetch_gmail_messages()
    return jsonify({"emails": emails})  

if __name__ == "__main__":
    app.run(port=8000, debug=True)  
