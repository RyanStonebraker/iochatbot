import uuid
from . import agent
from . import templateEngine

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
    templatingEngines = {
        "sad": None,
        "happy": None,
        "disgust": None,
        "angry": None
    }
    db = None

    def __init__(self, database):
        self.db = database
        self.agents["sad"] = agent.Agent(corpus="sadPoems.txt", verbose=False)
        self.templatingEngines["angry"] = templateEngine.TemplateEngine(corpus="friendsLines.txt", commonWords="angryWords.txt", emotion="angry")
        self.agents["angry"] = agent.Agent(corpus="generated/angry.txt", verbose=False, cacheCorpus=False)
        self.conversationUUID = str(uuid.uuid4())

    def getResponse(self, agentName, userInput):
        response = agentName
        if self.agents[agentName]:
            if self.templatingEngines[agentName]:
                self.templatingEngines[agentName].generateFile(userInput)
            response = self.agents[agentName].chat(userInput)

        self.conversationHistory[agentName].append({
            "userInput": userInput,
            "response": response
        })
        # self.db.collection(u'conversations').document(self.conversationUUID).set(self.conversationHistory)

        return response
