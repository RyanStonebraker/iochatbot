from flask import Flask, render_template, request
from chatbot import chatbot

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("insideoutchatbot-firebase-adminsdk-xmiwj-b04745e37d.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def chat():
    agents = [
        {
            "name": "angry",
            "response": ""
        },
        {
            "name": "sad",
            "response": ""
        },
        {
            "name": "happy",
            "response": ""
        },
        {
            "name": "disgust",
            "response": ""
        }
    ]
    query = ""
    if request.method == 'POST':
        for input, value in request.form.items():
            if input == "query":
                query = value
        for agent in agents:
            agent["response"] = environment.getResponse(agent["name"], query)

    return render_template("main.html", agents=agents, previousQuestion=query)


if __name__ == "__main__":
    environment = chatbot.Environment(db)
    app.run(debug=True, port=5001)
