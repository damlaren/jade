import random

labels = ["ope","con","ext","agr","neu","SWL","gender","age"]

input_files = [open("pic5_cleaned/all_" + label + ".txt","r") for label in labels]
filenames = ["pic5_cleaned/all_" + label + ".txt" for label in labels]
numfiles = len(input_files)

TRAINING_DIR = "pic5_cleaned/train/"
DEV_DIR = "pic5_cleaned/dev/"
TEST_DIR = "pic5_cleaned/test/"

for i in xrange(numfiles):
    lines = input_files[i].readlines()
    random.shuffle(lines)

    f1 = open(TRAINING_DIR + "train_" + labels[i] + ".txt", 'w')
    f2 = open(DEV_DIR + "dev_" + labels[i] + ".txt", 'w')
    f3 = open(TEST_DIR + "test_" + labels[i] + ".txt", 'w')

    temp = len(lines)
    for line in lines[:int(0.7*temp)]:
        f1.write(line)
    for line in lines[int(0.7*temp):int(0.85*temp)]:
        f2.write(line)
    for line in lines[int(0.85*temp):]:
        f3.write(line)
