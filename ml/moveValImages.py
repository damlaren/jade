
from os import listdir
from os.path import isfile, join, walk
import os as os

input_file = open("val.txt","r")

lines = input_file.readlines()

TRAINING_DIR = "/home/albert/Desktop/train/"
VAL_DIR = "/home/albert/Desktop/val/"

subfolders = ["32/","64/","128/","raw/","square/"]

for line in lines:
	tokens = line.strip().split(" ")
	for sf in subfolders:
		src = TRAINING_DIR + sf + tokens[0]
		dest = VAL_DIR + sf + tokens[0]
		os.rename(src, dest)