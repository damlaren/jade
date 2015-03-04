import os
import re
import shutil

FACES_DIR = "/home/albert/Desktop/pic5_dataset/faces/"
SINGLES_DIR = "/home/albert/Desktop/pic5_dataset/singles/"

labels_file = open("all_gender.txt","r")
single_labels_output_file = open("pic5_gender_all.txt","w")

lines = labels_file.readlines()



# This loop opens the FACES_DIR folder and counts the number of times
# a face appears per image.
file_list = os.listdir(FACES_DIR)
face_counts = {}

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


"""
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
"""

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


"""
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

"""

labels_file.close()
single_labels_output_file.close()