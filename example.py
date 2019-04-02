from agent import Agent

sadAgent = Agent(
    name = "Saddie", 
    corpus = "sadPoems.txt", 
    greetingMessage = "My name is Saddie The Sadbot. I'm an expert in sadness :(\nIf you want to leave, type 'bye'",
    defaultMessage = "Sorry.. I don't know what to say :(",
    goodbyeMessage = "Goodbye :("
)

sadAgent.chatCLI()

# testAgent = Agent()
# testAgent.chatCLI()