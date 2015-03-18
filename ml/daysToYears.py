

"""
Takes an input label file and converts the labels currently as days (ints)
into years (floats)
"""

input_file = open("/home/albert/Desktop/pic5_dataset/age/pic5_age_train.days.txt", "r")
output_file = open("/home/albert/Desktop/pic5_dataset/age/pic5_age_train.years.txt", "w")

lines = input_file.readlines()

for line in lines:
	tokens = line.strip().split(" ")
	days = int(tokens[1])
	years = int(1.0*days/365.25)
	output_file.write(tokens[0] + " " + str(years) + "\n")

input_file.close()
output_file.close()