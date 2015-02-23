from os import listdir
from os.path import isfile, join, walk
import os as os
import re

TRAINING_DIR = "/home/albert/Desktop/dsbowl15/train/"
TARGET_DIR = "/home/albert/Desktop/dsbowl15/train_all/"

output_file = open("training_labels.txt","w")

input_file = open("ClassLabels.csv","r")
lines = input_file.readlines()
clean_labels = []
for i, line in enumerate(lines):
	# Skip the header row of the CSV file
	if i == 0:
		continue
	tokens = line.strip().split(",")
	clean_labels.append(tokens[0])

folders = [x[0] for x in os.walk(TRAINING_DIR)]

for folder in folders:
	# training_folders includes the root for some reason
	if folder == TRAINING_DIR:
		continue
	# Output the class ID
	class_label = re.sub(TRAINING_DIR,'',folder)
	images = [ f for f in listdir(folder) if isfile(join(folder,f)) ]

	class_id = clean_labels.index(class_label)
	for image in images:
		os.rename(folder + "/" + image, TARGET_DIR + image)
		output_file.write(str(image) + " " + str(class_id) + "\n")

output_file.close()