import csv

def writeFile (header, fileName):
    with open(f'data/{fileName}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

def changeFile (data, fileName):
    currentData = []
    with open(f'data/{fileName}.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            currentData.append(row)
        currentData.append(data)
    with open(f'data/{fileName}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(currentData)

def readFile (fileName):
    with open(f'data/{fileName}.csv', newline='') as csvfile:
        readData = csv.DictReader(csvfile)
        data = []
        for row in readData:
            data.append(row)
        return data

    
    