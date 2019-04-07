import uuid
from . import agent as sadAgent

class Environment:
    conversationHistory = {
        "sad": [],
        "happy": [],
        "disgust": [],
        "angry": []
    }
    agents = {
        "sad": None,
        "happy": None,
        "disgust": None,
        "angry": None
    }
    db = None

    def __init__(self, database):
        self.db = database
        self.agents["sad"] = sadAgent.Agent(corpus="sadPoems.txt")
        self.conversationUUID = str(uuid.uuid4())

    def getResponse(self, agentName, userInput):
        response = agentName
        if self.agents[agentName]:
            response = self.agents[agentName].chat(userInput).replace("Chatbot: ", "")
            print(response)

        self.conversationHistory[agentName].append({
            "userInput": userInput,
            "response": response
        })
        # self.db.collection(u'conversations').document(self.conversationUUID).set(self.conversationHistory)

        return response
