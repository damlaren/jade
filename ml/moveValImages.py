
from os import listdir
from os.path import isfile, join, walk
import os as os

input_file = open("/home/albert/Desktop/pic5_dataset/pic5_gender_val.txt","r")

lines = input_file.readlines()

TRAINING_DIR = "/home/albert/Desktop/pic5_dataset/singles/"
VAL_DIR = "/home/albert/Desktop/pic5_dataset/val/"

"""
NOTE: The VAL_DIR must be created prior to running this script
"""

for line in lines:
	tokens = line.strip().split(" ")
	src = TRAINING_DIR + tokens[0]
	dest = VAL_DIR + tokens[0]
	# If file exists
	if os.path.isfile(src):
		os.rename(src, dest)