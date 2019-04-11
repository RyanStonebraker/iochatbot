import csv

with open("Andbrain_DataSet.csv", "r") as brainFile:
    brainReader = csv.reader(brainFile, delimiter=',')

    with open("disgust_words.txt", "w") as brainWriter:
        firstLine = True
        for line in brainReader:
            if firstLine:
                firstLine = False
                continue
            if float(line[1]) > .001:
                brainWriter.write(line[0] + "\n")