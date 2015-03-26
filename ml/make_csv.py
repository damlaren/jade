import re
import sys

if len(sys.argv) < 2:
    print "usage: python make_csv.py <log_file_1> [log_file_2] ..."
    sys.exit(1)

re_pattern = re.compile(".*Iteration (\d+).*loss = (\d*\.\d*)")

# extract log data
all_csv_data = {};
log_file_names = sys.argv[1 : len(sys.argv) + 1]
for log_file_name in log_file_names:
    print "Scanning %s" %(log_file_name)
    log_file = open(log_file_name, 'r')
    file_csv_data = {}
    for log_line in log_file:
        matches = re_pattern.match(log_line)
        if matches is not None:
            iteration = int(matches.group(1))
            loss = matches.group(2)
            if iteration <= 100:
                file_csv_data[iteration] = loss
    all_csv_data[log_file_name] = file_csv_data

# print the resulting csv
csv_file_name = 'losses.csv'
csv_file = open(csv_file_name, 'w')

# write header
csv_file.write("Iteration,")
for log_file_name in log_file_names:
    csv_file.write(log_file_name + ",")
csv_file.write("\n")

# content
for iteration in range (0, 100 + 1):
    line = str(iteration) + ","
    for log_file_name in log_file_names:
        file_csv_data = all_csv_data[log_file_name]
        line += str(file_csv_data[iteration]) + ","
    csv_file.write(line + "\n")
