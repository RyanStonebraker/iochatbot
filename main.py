from flask import Flask, render_template, request
from chatbot import chatbot

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
            agent["response"] = chatbot.getResponse(agent["name"], query)

    return render_template("main.html", agents=agents, previousQuestion=query)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
