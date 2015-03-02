import csv
import datetime

md5ind = 10
labels = ["ope","con","ext","agr","neu","SWL","gender","birthday"]
numlabels = len(labels)
today = datetime.date(2015, 1, 1)

# 8 is actually "birthday" in the csv
files = []
for label in labels:
    f = open("all_" + label + ".txt", 'w')
    files.append(f)

with open('data_2.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        for i in xrange(numlabels):
            if row[labels[i]] != 'NA':
                if labels[i] == "birthday":
                    d = datetime.date(int(row["birthday"][0:4]), int(row["birthday"][5:7]), int(row["birthday"][8:10]))
                    delta = today - d
                    files[i].write(row['md5'] + ".jpg " + str(delta.days) + '\n')
                else:
                    files[i].write(row['md5'] + ".jpg " + row[labels[i]] + '\n')

for f in files:
    f.close()
