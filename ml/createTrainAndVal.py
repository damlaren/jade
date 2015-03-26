
__author__ = "Albert Haque"
__date__ = 	"March 5, 2015"

import os
import re
import shutil
import time
import random
import numpy as np

"""
This script:
1. Takes an input folder of single face images
FOR A SPECIFIC PREDICTOR/LABEL (e.g. age, SWL, gender):
	2. Selects the images for which we have labels for (e.g. not all images have age labels)
	3. Creates a train and validation set and places the appropriate jpgs in each folder
		* The original singles input folder is unmodified
	4. Creates a training and validation labels file for the specified label

author: Albert Haque
"""

#######################################################################
# BEGIN REQUIRED INPUTS

# The labels to use: must be one of: (exact match)
# "age" "agr" "con" "ext" "gender" "neu" "ope" "SWL"
LABEL = "ext"

# This is the folder that contains the singles folder and where
# all subdatasets will be stored. A subdataset is the dataset (train/val)
# for a single label (e.g. age). See directory tree below
# Please include the slash at the end
FACES_ROOT = "/home/albert/Desktop/tophalf/"

"""
Output directory location. The folder structure will be like such:
FACES_ROOT
	|- singles
	|- age (will be created by this script)
	    |- train
	        |-- abcdefg12345.jpg
	        |--       :
	        |-- beadef987313.jpg
	    |- val
	        |-- abcdef111111.jpg
	        |--       :
	        |-- beade2222222.jpg
	    |- train.txt
	    |- val.txt

* Where "age" is replaced by the label you choose
* The "age" folder will be created by this script
"""

# Out of our entire dataset (with labels),
# how much should be allocated to the validation set
VAL_PERCENT = 0.1

# END REQUIRED INPUTS
#######################################################################

# Input folder consisting of ALL singles images
SINGLES_DIR = FACES_ROOT + "singles/"

# Input labels file
INPUT_LABELS_FILE = FACES_ROOT + "all_" + LABEL + ".txt"
SUBDATASET_ROOT = FACES_ROOT + LABEL + "/"

def extractImageId(filename):
	extension_start_index = filename.find(".")
	return filename[:extension_start_index]

# A class which keeps track of a filename, label pair
class DataPoint:
	def __init__(self, filename, label, label_type):
		self.filename = filename
		# Convert days to years
		if label_type == "age":
			# Caffe requires labels be integers (at least our setup does)
			self.label = int(1.0*int(label)/365.25)
		elif label_type == "gender":
			self.label = int(label)
		else:
			# Put data in the range of 1-100
			self.label = int(float(label)*10)

	def getFilename(self):
		return self.filename

	def getLabel(self):
		return self.label

	def __str__(self):
		return self.filename + " " + str(self.label)

############################################################
# SCRIPT BEGINS HERE
############################################################

print "Label:\t\t" + LABEL

# Get list of all files present in singles folder
singles_list1 = os.listdir(SINGLES_DIR)
singles_list2 = []

for filename in singles_list1:
	singles_list2.append(extractImageId(filename.replace(".aligned","")))

singles_list = set(singles_list2)

# Get the list of images in our labels file that are present in singles folder
# The ready_set is defined as the set of images for which we have labels for
# and each image only has a single face detection. This ready_set will be split
# into train and val
ready_set = []

input_file = open(INPUT_LABELS_FILE, "r")
lines = input_file.readlines()
num_lines = len(lines)

count = 0
found_count = 0
start_time = time.time()
for line in lines:
	tokens = line.strip().split(' ')
	imageid = extractImageId(tokens[0])
	# If this label does in fact have a single face detection
	if imageid in singles_list:
		dp = DataPoint(imageid, tokens[1], LABEL)
		ready_set.append(dp)
		found_count += 1

	count += 1
	if count % 100000 == 0:
		print "Scanned the labels file: " + str(count) + " / " + str(num_lines),
		print "Found: " + str(found_count) + "\tElapsed: " + str((time.time()-start_time))
input_file.close()

num_ready = len(ready_set)

# Create a train and validation set
np_ready_set = np.array(ready_set)
np.random.shuffle(np_ready_set)
val_size = int(num_ready*VAL_PERCENT)

validation_set = np_ready_set[0:val_size]
training_set = np_ready_set[val_size:]

print "Ready Size:\t" + str(len(ready_set))
print "Train Size:\t" + str(len(training_set))
print "Val Size:\t" + str(len(validation_set))

# Copy the images to the train/val folder
TRAIN_DIR = SUBDATASET_ROOT + "train/"
VAL_DIR = SUBDATASET_ROOT + "val/"

created_flag = False

if not os.path.exists(TRAIN_DIR):
    os.makedirs(TRAIN_DIR)
    print "Created the following directories:"
    print "\t" + TRAIN_DIR
    created_flag = True


if not os.path.exists(VAL_DIR):
    os.makedirs(VAL_DIR)
    if created_flag == False:
    	print "Created the following directories:"
    print "\t" + VAL_DIR

# Copy the images into their train/val folder and output to the labels file
train_labels_file = open(SUBDATASET_ROOT + LABEL + "_train.txt", "w")
val_labels_file = open(SUBDATASET_ROOT + LABEL + "_val.txt", "w")

print "Creating training set folder and labels..."
count = 0
start_time = time.time()
for dp in training_set:
	filename = dp.getFilename()
	src = SINGLES_DIR + filename + ".aligned.png"
	dest = TRAIN_DIR + filename + ".png"
	shutil.copy(src, dest)

	# Write the label to file
	train_labels_file.write(str(dp.filename) + ".png " + str(dp.label) + "\n")
	count += 1
	if count % 5000 == 0:
		print "Moved Training Images: " + str(count) + " / " + str(len(training_set)),
		print "\tElapsed: " + str((time.time()-start_time)) 

print "Finished moving training images!"
print "Creating validation set folder and labels..."

count = 0
start_time = time.time()
for dp in validation_set:
	filename = dp.getFilename()
	# Not all images end with face_0 for some reason...
	src = SINGLES_DIR + filename + ".aligned.png"
	dest = VAL_DIR + filename + ".png"
	shutil.copy(src, dest)

	# Write the label to file
	val_labels_file.write(str(dp.filename) + ".png " + str(dp.label) + "\n")
	count += 1
	if count % 5000 == 0:
		print "Moved Validation Images: " + str(count) + " / " + str(len(validation_set)),
		print "\tElapsed: " + str((time.time()-start_time)) 

print "Finished moving validation images!"
print "The script is complete and you may begin training."

train_labels_file.close()
val_labels_file.close()
