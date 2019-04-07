import datetime

from flask import Flask, render_template, request, make_response, jsonify
from chatbot import chatbot

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("insideoutchatbot-firebase-adminsdk-xmiwj-b04745e37d.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

global environment

validAgents = ["sad", "happy", "angry", "disgust"]

@app.route("/", methods = ['POST', 'GET'])
def chat():
    query = ""
    # if request.method == 'POST':
    #     for input, value in request.form.items():
    #         if input == "query":
    #             query = value
    #     for agent in agents:
    #         agent["response"] = environment.getResponse(agent["name"], query)

    return render_template("main.html", agents=validAgents, previousQuestion=query)

@app.route("/response", methods = ['POST', 'GET'])
def response():
    agent = {}
    if request.method == "GET":
        if request.args.get("agent") in validAgents:
            agent["name"] = request.args.get("agent")
            agent["response"] = environment.getResponse(request.args.get("agent"), request.args.get("query"))
    elif request.method == "POST":
        for input, value in request.form.items():
            if input == "query":
                query = value
            elif input == "agent" and value in validAgents:
                agent["name"] = value
        agent["response"] = environment.getResponse(agent["name"], query)

    return jsonify(agent)

if __name__ == "__main__":
    environment = chatbot.Environment(db)
    app.run(debug=True, port=5001)
