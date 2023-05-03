import csv
with open ('calendar.csv', newline='') as csvFile :
    spamreader = csv.reader(csvFile, delimiter=',')
    for row in spamreader:
        row[3] = row[3].replace("\r\n","")
        print(row)