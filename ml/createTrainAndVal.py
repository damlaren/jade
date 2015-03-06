
__author__ = "Albert Haque"
__date__ = 	"March 5, 2015"

import os
import re
import shutil
import time
import random

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
LABEL = "age"

# Make sure to specify the folder with a slash at the end
# Input folder consisting of ALL singles images
INPUT_SINGLES_DIR = "/Users/albert/Desktop/pic5_working/singles/"

# Input labels file (this is where you specify which predictor to use)
# Leave the "LABEL" at the end. You will probably just change the first part of the location
#INPUT_LABELS_FILE = "/Users/albert/Desktop/pic5_working/all_" + LABEL + ".txt"
INPUT_LABELS_FILE = "/Users/albert/Desktop/pic5_working/pic5_age_train.years.txt"

"""
Output directory location. The folder structure will be like such:
TARGET_DIR
	|- age
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

Where "age" is replaced by the label you choose
"""
TARGET_DIR = "/home/albert/Desktop/pic5_dataset/"

# Out of our entire dataset (with labels),
# how much should be allocated to the validation set
VAL_PERCENT = 0.05

# END REQUIRED INPUTS
#######################################################################

# A class which keeps track of a filename, label pair
class DataPoint:
	def __init__(self, filename, label, label_type):
		self.filename = filename
		# Convert days to years
		if label_type == "age":
			# Caffe requires labels be integers (at least our setup does)
			self.label = int(1.0*int(label)/365.25)
		else:
			self.label = int(float(label))

	def __str__(self):
		return self.filename + " " + str(label)

# Get list of all files present in singles folder
singles_list = os.listdir(INPUT_SINGLES_DIR)

# Get the list of images in our labels file that are present in singles folder
# The ready_set is defined as the set of images for which we have labels for
# and each image only has a single face detection. This ready_set will be split
# into train and val
ready_set = []

input_file = open(INPUT_LABELS_FILE, "r")
lines = input_file.readlines()

count = 0
start_time = time.time()
for line in lines:
	tokens = line.strip().split(' ')
	# If this label does in fact have a single face detection
	if tokens[0] in singles_list:
		dp = DataPoint(tokens[0], tokens[1], LABEL)
		ready_set.append(dp)

	count += 1
	if count % 10000 == 0:
		print "Creating Ready Set. Scanned: " + str(count) + "\tElapsed: " + str((time.time()-start_time))
input_file.close()

NUM_READY = len(ready_set)
print "Num Images in Ready Set: " + str(NUM_READY)

# Create a train and validation set
randomized_ready_set = random.shuffle(ready_set)
val_size = int(NUM_READY*VAL_PERCENT)
print val_size

# Copy the images to the train/val folder


# Output the train/val labels

"""

lines = INPUT_LABELS_FILE.readlines()

# This loop opens the FACES_DIR folder and counts the number of times
# a face appears per image.
file_list = os.listdir(FACES_DIR)

for filename in file_list:
	# If file is a txt or cfidu, ignore it
	if "cfidu" in filename or "txt" in filename:
		continue
	id_end_index = filename.index('_')
	user_id = filename[:id_end_index]
	if user_id in face_counts:
		face_counts[user_id] += 1
	else:
		face_counts[user_id] = 1

# Get the list of user_ids with single face detection
single_user_ids = []
for key in face_counts:
	if face_counts[key] == 1:
		single_user_ids.append(key)


# Copy the .jpg files to the singles folder
for filename in single_user_ids:
	# Not all images end with face_0 for some reason...
	for i in xrange(0, 5):
		src = FACES_DIR + filename + "_face_" + str(i) + ".jpg"
		if os.path.isfile(src):
			break
	count += 1
	dest = SINGLES_DIR + filename + ".jpg"
	shutil.copy(src, dest)


# Create a labels file consisting of the single images only
# This loop below reads the gender labels for the ENTIRE dataset into gender_labels
gender_labels = {}
for line in lines:
	tokens = line.strip().split(' ')
	gender_labels[tokens[0]] = int(tokens[1])

# Only write the single labels. We then loop through our
# singles array and get the correct label from the ALL gender_labels dict
for key in single_user_ids:
	key = key + ".jpg"
	# Some user_ids won't have a gender label
	if key not in gender_labels:
		continue
	# Write to file
	single_labels_output_file.write(key + " " + str(gender_labels[key]) + "\n")


# Creates and prints out the histogram (this code works perfectly fine)
# If you're curious about how many images we lost, etc.

histogram_output_file = open("histogram.csv", "w")
histogram = {}
for key in face_counts:
	#histogram_output_file.write(key + "," + str(face_counts[key]) + "\n")
	if face_counts[key] not in histogram:
		histogram[face_counts[key]] = 1
	else:
		histogram[face_counts[key]] += 1

print histogram
histogram_output_file.close()


labels_file.close()
single_labels_output_file.close()

"""