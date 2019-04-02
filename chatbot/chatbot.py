from . import agent

def getResponse(agentName, userInput):
    response = agentName
    if agentName == "sad":
        sadAgent = agent.Agent()
        response = sadAgent.chat(userInput).replace("Chatbot: ", "")
    return response
