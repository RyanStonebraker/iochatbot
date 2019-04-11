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

def switchPronouns(word):
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

def identifySubjects(categorizedSentence):
    subjects = []
    nounType = ["PRP", "PRP$", "NN", "NNS", "NNP", "NNPS"]
    for word, type in categorizedSentence:
        if type in nounType:
            word = switchPronouns(word)
            subjects.append(word)
    return subjects

def tagDataset(dataset):
    taggedData = []
    for sentence in dataset:
        taggedData.append(nltk.pos_tag(sentence.lower().split(" ")))
    return taggedData

def simplifyLabels(words):
    simplifiedLabels = {
        "noun": [],
        "verb": [],
        "adjective": []
    }
    taggedWords = tagDataset(words)

    nounType = ["PRP", "PRP$", "NN", "NNS", "NNP", "NNPS"]
    adjectiveType = ["JJ", "JJR", "JJS"]
    verbType = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

    for taggedWord in taggedWords:
        for word, type in taggedWord:
            if type in nounType:
                simplifiedLabels["noun"].append(word)
            elif type in adjectiveType:
                simplifiedLabels["adjective"].append(word)
            elif type in verbType:
                simplifiedLabels["verb"].append(word)

    return simplifiedLabels

def chooseSentenceTemplate(subjects, templates):
    for sentence in templates:
        templateSubjects = identifySubjects(sentence)
        matchingSubjectCount = 0
        for subject in templateSubjects:
            if subject in subjects:
                matchingSubjectCount += 1
                sentenceProbability = 100 * (1 - 1/(1 + matchingSubjectCount))
                if random.randint(1, 100) > sentenceProbability:
                    return sentence

    return random.choice(templates)

def replaceContextWord(associatedWords, currentWord, subjects, type, mutation=80, lastWord=""):
    if random.randint(1, 100) > mutation:
        for _ in range(0, 5):
            randomAssociatedWord = random.choice(associatedWords[type])
            if randomAssociatedWord != lastWord:
                return random.choice(associatedWords[type])
    else:
        randomSubject = random.choice(subjects)
        return randomSubject if lastWord != randomSubject else currentWord


def inferTemplateContext(subjects, template, associatedWords):
    response = []

    nounType = ["PRP", "PRP$", "NN", "NNS", "NNP", "NNPS"]
    adjectiveType = ["JJ", "JJR", "JJS"]
    verbType = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

    for word, type in template:
        lastWord = response[-1] if len(response) else ""
        if type in nounType:
            response.append(replaceContextWord(associatedWords, word, subjects, "noun", 60, lastWord))
        elif type in adjectiveType:
            response.append(replaceContextWord(associatedWords, word, [word], "adjective", 85, lastWord))
        elif type in verbType:
            response.append(replaceContextWord(associatedWords, word, [word], "verb", 60, lastWord))
        else:
            response.append(word)

    return " ".join(response)

if __name__ == "__main__":
    nltk.download('averaged_perceptron_tagger')
    nltk.download('tagsets')
    # Remove punctuation, lowercase
    sentence = input("Enter: ").lower()
    sentence = sentence.translate(str.maketrans('', '', string.punctuation)).split(" ")
    categorizedSentence = nltk.pos_tag(sentence)

    subjects = identifySubjects(categorizedSentence)

    templates = tagDataset(sampleSentences)
    associatedWords = simplifyLabels(commonAngryWords)

    template = chooseSentenceTemplate(subjects, templates)
    response = inferTemplateContext(subjects, template, associatedWords)

    print(response)
