import csv

# Membaca file .csv 
# data.csv = roomID,Name,Contact,roomType,Price,daysofStay
def csvReader():
    rooms = []
    with open('data.csv', 'r') as data:
        reader = csv.DictReader(data)
        for line in reader:
            rooms.append(line)
            print(line)
    return rooms           
            
class List:
    def __init__(self, roomID, guestName, guestContact, roomType, Price, daysofStay):
        self.roomID = roomID
        self.guestName = guestName
        self.guestContact = guestContact
        self.roomType = roomType
        self.Price = Price
        self.daysofStay = daysofStay
    
    def getList(self):
        return {
            "roomID": self.roomID,
            "Name": self.guestName,
            "Contact": self.guestContact,
            "roomType": self.roomType,
            "Price": self.Price,
            "daysofStay": self.daysofStay
        }
     
class RoomBooking:
    def __init__(self):
        self.data = csvReader()         

aji = List('roomID', 'Name',  'Contact', 'roomType', 'Price', 'dayofStay')
print(aji.getList())