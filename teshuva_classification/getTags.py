import os

# modify this code to write to a file instead of creating an array
# split the data into testing and training
sentences = []
rootdir = "/Users/adinacohen/Documents/Stern/Stern Senior Year/Thesis/teshuva_classification/BYAnnotation"
trainOutput = open("trainTaggedText.txt", 'w', encoding='utf-8')
devOutput = open("devTaggedText.txt", 'w', encoding='utf-8')
fileCount = 0

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        f = open((subdir + "/" + file), 'r', encoding='utf-8')
        s = []
        for line in f:
            line = line.split('\t')
            if len(line) > 3:
                word, tag = line[2], line[3]
                if tag.startswith('Citation\_Introduction'):
                    tag = 'Citation_Introduction'
                elif tag.startswith('Citation'):
                    tag = 'Citation'
                if fileCount > 13:
                    devOutput.write(word + "\t" + tag + "\n")
                else:
                    trainOutput.write(word + "\t" + tag + "\n")

        f.close()
        fileCount += 1

trainOutput.close()
devOutput.close()


