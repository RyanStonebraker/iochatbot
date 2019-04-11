import nltk
import numpy as np
import random
import string
import re

# Term Frequency-Inverse Document Frequency (TF-IDF)
# This bag of words heuristic weighs word scores based on the total number of docs
# over how many docs the word appears in, effectively discarding biases for popular
# words like 'the'.
from sklearn.feature_extraction.text import TfidfVectorizer

# Cosine similarity
# Used to find the similarity between user input and words in the corpora
from sklearn.metrics.pairwise import cosine_similarity

# ELIZA just uses keyword matching for greetings:
USER_GREETINGS = ("hello", "hi", "greetings", "sup", "what's up", "hey", "heyo", "what up", "yo")
AGENT_RESPONSES = ("hello, human", "hi", "oh.. hi there", "hello", "hi... I'm a little shy", "hello... I'm not very good at conversations")

# Percepts = user input
# Environment = Corpus/GUI Input
# Action = Return response string
# Sensors =
#   * Get input from user (if running CLI version)
#   * Recieve input from GUI through input field
# Agent = Emotions: Happy, Disgust, Angry, Sad
# Actuators =

class Agent:
    corporaDirectory = "chatbot/corpora"

    def __init__(
        self,
        name="Chatbot",
        corpus='default.txt',
        greetingMessage="My name is {0} The Chatbot!\nIf you want to leave, type 'bye'",
        defaultMessage="Sorry, I don't understand.",
        goodbyeMessage="See ya later!",
        verbose=True,
        cacheCorpus=True
        ):
        self.name = name
        self.corpus = corpus
        self.greetingMessage = greetingMessage.format(self.name)
        self.defaultMessage = defaultMessage
        self.goodbyeMessage = goodbyeMessage
        self.verbose = verbose
        self.cacheCorpus = cacheCorpus

        if self.cacheCorpus:
            self.loadCorpus()

        nltk.download('punkt')
        nltk.download('wordnet')

        # Tokenization and normalization handlers
        self.lemmer = nltk.stem.WordNetLemmatizer()
        self.removePunctuation = dict((ord(punct), None) for punct in string.punctuation)

        self.introduction()

    def loadCorpus(self):
        with open("{0}/{1}".format(self.corporaDirectory, self.corpus), "r") as corpusFile:
            self.environment = re.sub(r"\s+", " ", corpusFile.read().lower())

        self.corpusSentencesActuator = nltk.sent_tokenize(self.environment)
        self.corpusWordsActuator = nltk.word_tokenize(self.environment)


    def introduction(self):
        if self.verbose:
            welcomeMessage  = "**********************************\n"
            welcomeMessage += "***** Inside Out Chatbot CLI *****\n"
            welcomeMessage += "**********************************\n"
            print(welcomeMessage)
            print(self.greetingMessage)

    def lemanizeTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def normalize(self, text):
        return self.lemanizeTokens(nltk.word_tokenize(text.lower().translate(self.removePunctuation)))

    def greeting(self, userInput):
        for word in userInput.split():
            if word.lower() in USER_GREETINGS:
                return random.choice(AGENT_RESPONSES)

    def response(self, userInput):
        agentResponse=''
        self.corpusSentencesActuator.append(userInput)

        # Stop words are words that do not contribute to the understanding of text
        # Here, we are using a predefined list of such words.
        TfidfVector = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')
        termFrequencies = TfidfVector.fit_transform(self.corpusSentencesActuator)
        similarities = cosine_similarity(termFrequencies[-1], termFrequencies)
        corpusSentencesIndex = similarities.argsort()[0][-2]
        flat = similarities.flatten()
        flat.sort()
        resultantTermFrequency = flat[-2]

        if (resultantTermFrequency == 0):
            agentResponse = agentResponse + self.defaultMessage
            self.corpusSentencesActuator.remove(userInput)
            return agentResponse
        else:
            agentResponse = agentResponse + self.corpusSentencesActuator[corpusSentencesIndex]
            self.corpusSentencesActuator.remove(userInput)
            return agentResponse

    def sense(self):
        userInputPercept = input()
        userInputPercept = userInputPercept.lower()
        return userInputPercept

    def action(self, userInputPercept):
        response = ""
        if (userInputPercept != "bye"):
            greeting = self.greeting(userInputPercept)
            response = greeting if greeting else self.response(userInputPercept) + "\n"
        else:
            response = self.goodbyeMessage

        return response

    def chatCLI(self):
        while True:
            userInputPercept = input("Chat: ")
            userInputPercept = userInputPercept.lower()

            print("{0}: {1}".format(self.name, self.action(userInputPercept)))

            if(userInputPercept == "bye"):
                break

    # To be used with the GUI
    #
    # Note: sensing is performed on the GUI
    #       through the input field if this
    #       member function is being used.
    #
    def chat(self, userInputPercept):
        if not self.cacheCorpus:
            self.loadCorpus()
        return self.action(userInputPercept)
