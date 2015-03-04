import os
import re
import shutil

FACES_DIR = "/home/albert/Desktop/pic5_dataset/faces/"
SINGLES_DIR = "/home/albert/Desktop/pic5_dataset/singles/"

labels_file = open("all_gender.txt","r")
output_file = open("histogram.csv", "w")

lines = labels_file.readlines()

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

count = 0
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
print count
# Copy the labels to the singles folder

"""
# Creates and prints out the histogram (this code works perfectly fine)
histogram = {}
for key in face_counts:
	#output_file.write(key + "," + str(face_counts[key]) + "\n")
	if face_counts[key] not in histogram:
		histogram[face_counts[key]] = 1
	else:
		histogram[face_counts[key]] += 1

print histogram
"""

output_file.close()
labels_file.close()
