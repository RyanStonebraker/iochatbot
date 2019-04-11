import nltk
import string
import random

sampleSentences = [
    "I am doing great.",
    "The world outside is nice.",
    "I want to punch something.",
    "Yellow is the color of happiness.",
    "I'm sorry I hurt your feelings when I called you stupid. I honestly thought you already knew.",
    "Pissed off that Spotify isn't an app that turns you into a leopard."
]

commonAngryWords = [
    "angry",
    "mad",
    "bad",
    "stupid",
    "fire",
    "red",
    "punch",
    "fist",
    "pissed"
]

class AngryBot():
    def __init__(self, corpus="", commonWords=""):
        nltk.download('averaged_perceptron_tagger')
        nltk.download('tagsets')

        self.nounType = ["PRP", "PRP$", "NN", "NNS", "NNP", "NNPS"]
        self.adjectiveType = ["JJ", "JJR", "JJS"]
        self.verbType = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

        self.templates = self.tagDataset(sampleSentences)
        self.associatedWords = self.simplifyLabels(commonAngryWords)

    def switchPronouns(self, word):
        swapList = [
            ("you", "I"),
            ("your", "my"),
            ("yours", "mine")
        ]
        for firstSide, secondSide in swapList:
            if word == firstSide:
                word = secondSide
            elif word == secondSide:
                word = firstSide
        word = word.replace("me", "you")

        return word

    def identifySubjects(self, categorizedSentence):
        subjects = []
        for word, type in categorizedSentence:
            if type in self.nounType:
                word = self.switchPronouns(word)
                subjects.append(word)
        return subjects

    def tagDataset(self, dataset):
        taggedData = []
        for sentence in dataset:
            taggedData.append(nltk.pos_tag(sentence.lower().split(" ")))
        return taggedData

    def simplifyLabels(self, words):
        simplifiedLabels = {
            "noun": [],
            "verb": [],
            "adjective": []
        }
        taggedWords = self.tagDataset(words)

        for taggedWord in taggedWords:
            for word, type in taggedWord:
                if type in self.nounType:
                    simplifiedLabels["noun"].append(word)
                elif type in self.adjectiveType:
                    simplifiedLabels["adjective"].append(word)
                elif type in self.verbType:
                    simplifiedLabels["verb"].append(word)

        return simplifiedLabels

    def chooseSentenceTemplate(self, subjects):
        for sentence in self.templates:
            templateSubjects = self.identifySubjects(sentence)
            matchingSubjectCount = 0
            for subject in templateSubjects:
                if subject in subjects:
                    matchingSubjectCount += 1
                    sentenceProbability = 100 * (1 - 1/(1 + matchingSubjectCount))
                    if random.randint(1, 100) > sentenceProbability:
                        return sentence

        return random.choice(self.templates)

    def replaceContextWord(self, currentWord, subjects, type, mutation=80, lastWord=""):
        if random.randint(1, 100) > mutation:
            for _ in range(0, 5):
                randomAssociatedWord = random.choice(self.associatedWords[type])
                if randomAssociatedWord != lastWord:
                    return random.choice(self.associatedWords[type])
        else:
            randomSubject = random.choice(subjects)
            return randomSubject if lastWord != randomSubject else currentWord


    def inferTemplateContext(self, subjects, template):
        response = []

        for word, type in template:
            lastWord = response[-1] if len(response) else ""
            if type in self.nounType:
                response.append(self.replaceContextWord(word, subjects, "noun", 60, lastWord))
            elif type in self.adjectiveType:
                response.append(self.replaceContextWord(word, [word], "adjective", 85, lastWord))
            elif type in self.verbType:
                response.append(self.replaceContextWord(word, [word], "verb", 60, lastWord))
            else:
                response.append(word)

        return " ".join(response)

    def chat(self, userInput):
        userInput = userInput.translate(str.maketrans('', '', string.punctuation)).split(" ")
        categorizedSentence = nltk.pos_tag(userInput)

        subjects = self.identifySubjects(categorizedSentence)
        template = self.chooseSentenceTemplate(subjects)

        return self.inferTemplateContext(subjects, template)

if __name__ == "__main__":
    bot = AngryBot()
    userInput = input("Enter: ")

    print(bot.chat(userInput))
