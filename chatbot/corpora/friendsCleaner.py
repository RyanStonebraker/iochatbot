import csv

with open("friendsCorpus.txt", "r") as friendFile:
    friendReader = csv.reader(friendFile, delimiter='\t')

    with open("friendsLines.txt", "w") as friendWriter:
        for line in friendReader:
            friendWriter.write(line[5] + "\n")
