import csv
from collections import Counter


with open('data/newdata.csv', 'r') as data_file:
    data = csv.reader(data_file, delimiter=',')

    labels = [row[3] for row in data]

    for (k, v) in Counter(labels).items():
        with open('data/labeldata.csv', 'a') as file:
            writer = csv.writer(file)
            row_data = [k, v]
            writer.writerow(row_data)
            file.close()
        print("%s, %d" % (k, v))