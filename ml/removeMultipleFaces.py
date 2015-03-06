import os
import re
import shutil
import time

FACES_DIR = "/home/ec2-user/faces/"
SINGLES_DIR = "/home/ec2-user/singles/"

# This loop opens the FACES_DIR folder and counts the number of times
# a face appears per image.
file_list = os.listdir(FACES_DIR)
face_counts = {}

print "Building the face count dictionary..."
count = 0
start_time = time.time()
for filename in file_list:
	id_end_index = filename.index('_')
	user_id = filename[:id_end_index]
	if user_id in face_counts:
		face_counts[user_id] += 1
	else:
		face_counts[user_id] = 1
	count += 1
	if count % 100000 == 0:
		print "Built Dictionary: " + str(count) + "\tElapsed: " + str((time.time()-start_time))

# Get the list of user_ids with single face detection
count = 0
print "Identifying single images..."
start_time = time.time()
single_user_ids = []
for key in face_counts:
	if face_counts[key] == 1:
		single_user_ids.append(key)
	count += 1
	if count % 10000 == 0:
		print "Identifying Single Images, Scanned: " + str(count) + "\tElapsed: " + str((time.time()-start_time))

print "Copying images into the singles directory..."

# Copy the .jpg files to the singles folder
count = 0
start_time = time.time()
for filename in single_user_ids:
	# Not all images end with face_0 for some reason...
	for i in xrange(0, 10):
		src = FACES_DIR + filename + "_face_" + str(i) + ".jpg"
		if os.path.isfile(src):
			break
	dest = SINGLES_DIR + filename + ".jpg"
	shutil.copy(src, dest)
	count += 1
	if count % 10000 == 0:
		print "Copied Single Images: " + str(count) + " / " + str(len(single_user_ids)) + "\tElapsed: " + str((time.time()-start_time))

# Creates and prints out the histogram (this code works perfectly fine)
# If you're curious about how many images we lost, etc.

histogram = {}
for key in face_counts:
	#histogram_output_file.write(key + "," + str(face_counts[key]) + "\n")
	if face_counts[key] not in histogram:
		histogram[face_counts[key]] = 1
	else:
		histogram[face_counts[key]] += 1

print histogram
