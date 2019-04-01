from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    agentNames = [
        "angry",
        "sad",
        "happy",
        "disgust"
    ]

    agents = [
        {
            "name": "angry",
            "response": "testing angry response"
        },
        {
            "name": "sad",
            "response": "testing sad response"
        },
        {
            "name": "happy",
            "response": "testing happy response"
        },
        {
            "name": "disgust",
            "response": "testing disgust response"
        }
    ]
    return render_template("main.html", agents=agents)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
