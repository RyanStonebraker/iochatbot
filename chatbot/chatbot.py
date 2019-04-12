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

        self.templatingEngines["sad"] = templateEngine.TemplateEngine(corpus="sadFriendsTemplates.txt", commonWords="sadWords.txt", emotion="sad")
        self.agents["sad"] = agent.Agent(corpus="generated/sad.txt", verbose=False, cacheCorpus=False, defaultMessage="Maybe. What about you?")

        self.templatingEngines["angry"] = templateEngine.TemplateEngine(corpus="angryFriendsTemplates.txt", commonWords="angryWords.txt", emotion="angry")
        self.agents["angry"] = agent.Agent(corpus="generated/angry.txt", verbose=False, cacheCorpus=False, defaultMessage="Are you?")

        self.templatingEngines["happy"] = templateEngine.TemplateEngine(corpus="happyFriendsTemplates.txt", commonWords="happyWords.txt", emotion="happy")
        self.agents["happy"] = agent.Agent(corpus="generated/happy.txt", verbose=False, cacheCorpus=False, defaultMessage="What about you?")

        self.templatingEngines["disgust"] = templateEngine.TemplateEngine(corpus="disgustFriendsTemplates.txt", commonWords="disgust_words.txt", emotion="disgust")
        self.agents["disgust"] = agent.Agent(corpus="generated/disgust.txt", verbose=False, cacheCorpus=False, defaultMessage="Definitely not. Are you?")

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
