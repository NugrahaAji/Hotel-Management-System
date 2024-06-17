import csv

# Membaca file .csv 
# data.csv = roomID,Name,Contact,roomType,Price,daysofStay
def csvReader(var):
    with open('data.csv','r') as data:
        reader = csv.DictReader(data)
        for line in reader:
            print(line[var])           

while True:
    choose = int(input("1. Room ID\n2. Room Type\n3. Name\n"))
    if choose == 1:
        csvReader('roomID')
    elif choose == 2:
        csvReader('roomType')
    elif choose == 3:
        csvReader('Name')
    else: break