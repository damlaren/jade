
input_file = open("/home/albert/caffe/tophalf_gender.log","r")
output_file = open("tophalf_accuracy.csv","w")


lines = input_file.readlines()

epochNum = 0
test_acc = 0
train_acc = 0
for line in lines:
	if "Test net output #0" in line:
		equals_index = line.find("=")
		test_acc = float(line[equals_index+2:])
	elif "Train net output #0" in line:
		equals_index = line.find("=")
		train_acc = float(line[equals_index+2:])
	if test_acc > 0 and train_acc > 0:
		output_file.write(str(epochNum) + "," + str(train_acc) + "," + str(test_acc) + "\n")
		print epochNum, train_acc, test_acc
		train_acc = 0
		test_acc = 0