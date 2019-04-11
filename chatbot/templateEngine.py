import nltk
import string
import random

class TemplateEngine():
    def __init__(self, corpus="angrySentences.txt", commonWords="angryWords.txt", emotion="angry"):
        nltk.download('averaged_perceptron_tagger')
        nltk.download('tagsets')

        self.emotion = emotion
        self.corporaDirectory = "chatbot/corpora"

        self.nounType = ["PRP", "PRP$", "NN", "NNS", "NNP", "NNPS"]
        self.adjectiveType = ["JJ", "JJR", "JJS"]
        self.verbType = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

        with open("{0}/{1}".format(self.corporaDirectory, corpus), "r") as corpusReader:
            rawCorpus = corpusReader.read().replace("\n", " ").strip().split(".")
            rawCorpus = [angrySentence for angrySentence in rawCorpus if angrySentence]
            self.templates = self.tagDataset(rawCorpus)

        with open("{0}/{1}".format(self.corporaDirectory, commonWords), "r") as commonWordReader:
            commonWords = [line.strip().replace("\n", "") for line in commonWordReader.readlines()]
            self.associatedWords = self.simplifyLabels(commonWords)

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
            try:
                taggedSentence = nltk.pos_tag(sentence.strip().lower().split(" "))
                taggedData.append(taggedSentence)
            except:
                continue
        return taggedData

    def simplifyLabels(self, words):
        simplifiedLabels = {
            # "noun": [],
            # "verb": [],
            # "adjective": []
        }
        taggedWords = self.tagDataset(words)

        for taggedWord in taggedWords:
            for word, type in taggedWord:
                if type in simplifiedLabels:
                    simplifiedLabels[type].append(word)
                else:
                    simplifiedLabels[type] = [word]
                # if type in self.nounType:
                #     simplifiedLabels["noun"].append(word)
                # elif type in self.adjectiveType:
                #     simplifiedLabels["adjective"].append(word)
                # elif type in self.verbType:
                #     simplifiedLabels["verb"].append(word)

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

        for _ in range(0, 5):
            randomTemplate = random.choice(self.templates)
            if randomTemplate:
                return randomTemplate
        return randomTemplate

    def replaceContextWord(self, currentWord, subjects, type, mutation=80, lastWord=""):
        if type in self.associatedWords and random.randint(1, 100) < mutation:
            for _ in range(0, 5):
                randomAssociatedWord = random.choice(self.associatedWords[type])
                if randomAssociatedWord != lastWord:
                    return random.choice(self.associatedWords[type])
        else:
            randomSubject = random.choice(subjects)
            return randomSubject if lastWord != randomSubject else currentWord


    def inferTemplateContext(self, subjects, template):
        response = []

        replaceTypes = {
            "NN": 60,
            "NNS": 60,
            "NNP": 60,
            "NNPS": 60,
            "PRP": 60,
            "PRP$": 60,
            "VB": 50,
            "VBD": 50,
            "VBG": 50,
            "VBN": 50,
            "VBP": 50,
            "VBZ": 50,
            "JJ": 75,
            "JJR": 75,
            "JJS": 75
        }

        for word, type in template:
            lastWord = response[-1] if len(response) else ""
            if type in replaceTypes:
                defaultOptions = subjects if type in self.nounType else [word]
                response.append(self.replaceContextWord(word, defaultOptions, type, replaceTypes[type], lastWord))
            # if type in self.nounType:
            #     response.append(self.replaceContextWord(word, subjects, "noun", 60, lastWord))
            # elif type in self.adjectiveType:
            #     response.append(self.replaceContextWord(word, [word], "adjective", 75, lastWord))
            # elif type in self.verbType:
            #     response.append(self.replaceContextWord(word, [word], "verb", 60, lastWord))
            else:
                response.append(word)
        sentenceResponse = " ".join(response)
        return sentenceResponse

    def chat(self, userInput):
        userInput = userInput.translate(str.maketrans('', '', string.punctuation)).split(" ")
        categorizedSentence = nltk.pos_tag(userInput)

        subjects = self.identifySubjects(categorizedSentence)
        template = self.chooseSentenceTemplate(subjects)

        return self.inferTemplateContext(subjects, template)

    def generateFile(self, userInput):
        with open("{0}/generated/{1}".format(self.corporaDirectory, "{0}.txt".format(self.emotion)), "w") as emoFile:
            userInput = userInput.translate(str.maketrans('', '', string.punctuation)).split(" ")
            categorizedSentence = nltk.pos_tag(userInput)

            subjects = self.identifySubjects(categorizedSentence)

            for _ in range(0, 100):
                template = self.chooseSentenceTemplate(subjects)
                try:
                    response = self.inferTemplateContext(subjects, template) + ".\n"
                    emoFile.write(response)
                except:
                    continue

if __name__ == "__main__":
    bot = TemplateEngine(corpus="friendsLines.txt")
    userInput = input("Enter: ")

    bot.generateFile(userInput)
