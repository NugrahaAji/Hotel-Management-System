import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
tree = None
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
width = 855
height = 540
newX = int((screenwidth/2)-(width/2))
newY = int((screenheight/2)-(height/2))

def csvReader():
    rooms = []
    with open('data.csv', 'r') as data:
        reader = csv.DictReader(data)
        for line in reader:
            rooms.append(line)
    return rooms

def binarySearch(arr, target_name):
    left, right = 0, len(arr) - 1
    target_name = target_name.lower()

    while left <= right:
        mid = (left + right) // 2
        current_name = arr[mid].guestName.lower()

        if current_name == target_name:
            return mid
        elif current_name < target_name:
            left = mid + 1
        else:
            right = mid - 1

    return False

class List:
    def __init__(self, roomID, guestName, guestContact, roomType, Price, daysofStay, Date):
        self.roomID = roomID
        self.guestName = guestName
        self.guestContact = guestContact
        self.roomType = roomType
        self.Price = Price
        self.daysofStay = daysofStay
        self.Date = Date

class RoomManager:
    def __init__(self):
        self.rooms = csvReader()
        self.roomList = sorted(
            [List(
                room['roomID'],
                room['Name'],
                room['Contact'],
                room['roomType'],
                room['Price'],
                room['daysofStay'],
                room['Date']
            ) for room in self.rooms],
            key=lambda x: x.guestName.lower()
        )

    def roomReserve(self, roomID, firstName, lastName, contact, daysOfStay, date):
        Update = []
        reader = csvReader()
        for room in reader:
            if room['roomID'] == roomID:
                fullName = f"{firstName} {lastName}"
                room['Name'] = fullName
                room['Contact'] = contact
                room['daysofStay'] = int(daysOfStay)
                room['Date'] = date
            Update.append(room)

        with open('data.csv', 'w', newline='') as file:
            fieldnames = ['roomID', 'Name', 'Contact', 'roomType', 'Price', 'daysofStay', 'Date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(Update)

    def roomRemove(self, roomID):
        Update = []
        reader = csvReader()
        for room in reader:
            if room['roomID'] == roomID and room['Name'] != '-':
                room['Name'] = '-'
                room['Contact'] = '-'
                room['daysofStay'] = '-'
                room['Date'] = '-'
            Update.append(room)

        with open('data.csv', 'w', newline='') as file:
            fieldnames = ['roomID', 'Name', 'Contact', 'roomType', 'Price', 'daysofStay', 'Date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(Update)

    def calculateBill(self, roomID):
        for room in self.rooms:
            if roomID == room['roomID']:
                try:
                    price = int(room['Price'])
                    days = int(room['daysofStay'])
                    return price * days
                except ValueError:
                    return None
        return False
    
    def getReservedRoomID(self):
        reservedRoomID = [room.roomID for room in self.roomList if room.guestName != '-']
        return reservedRoomID

    def getunReservedRoomID(self):
        unReservedRoomID = [room.roomID for room in self.roomList if room.guestName == '-']
        return unReservedRoomID
    
    def searchGuestName(self, keyword):
        keyword = keyword.lower()
        keywordRoomID = binarySearch(self.roomList, keyword)
        if keywordRoomID != False:
            return self.roomList[keywordRoomID]
        else:
            return None

def MainWindow():
    global tree
    for widget in root.winfo_children():
        widget.destroy()

    rooms = csvReader()
    roomList = [List(
        room['roomID'],
        room['Name'],
        room['Contact'],
        room['roomType'],
        room['Price'],
        room['daysofStay'],
        room['Date']
    ) for room in rooms]

    main = RoomManager()
    
    reservedRoomID = main.getReservedRoomID()
    reservedRooms = [room for room in roomList if room.roomID in reservedRoomID]
    
    unReservedRoomID = main.getunReservedRoomID()
    unReservedRooms = [room for room in roomList if room.roomID in unReservedRoomID]

    TableFrame = ttk.Frame(root)
    TableFrame.pack(side=tk.LEFT, padx=(20, 0), pady=20, expand=False, fill='both')

    ButtonFrame = ttk.Frame(root)
    ButtonFrame.pack(side=tk.RIGHT, padx = (0,20), pady=20, fill='both')

    RoomLabel = ttk.Label(ButtonFrame, text = 'Show Rooms')
    RoomLabel.pack(padx=5, pady=5)
    showAllButton = ttk.Button(ButtonFrame, text="All Rooms", command=MainWindow)
    showAllButton.pack(padx=5, pady=5)

    showReservedButton = ttk.Button(ButtonFrame, text="Reserved", command=lambda: showContent(reservedRooms))
    showReservedButton.pack(padx=5, pady=5)

    showunReservedButton = ttk.Button(ButtonFrame, text="Unreserved",command=lambda: showContent(unReservedRooms))
    showunReservedButton.pack(padx=5, pady=5)

    UpdateLabel = ttk.Label(ButtonFrame, text = 'Room Update')
    UpdateLabel.pack(padx=5, pady=(30,0))
    reserveButton = ttk.Button(ButtonFrame, text = "Reserve", command=lambda: ReserveWindow())
    reserveButton.pack(padx=5, pady=5)

    removeButton = ttk.Button(ButtonFrame, text = "Remove", command=lambda: RemoveWindow())
    removeButton.pack(padx=5, pady=5)

    sortRoomIDButton = ttk.Button(ButtonFrame, text="Sort by ID")
    sortRoomIDButton.pack(side=tk.BOTTOM, padx=5, pady=(5,5))

    sortedDateButton = ttk.Button(ButtonFrame, text = "Sort by Price")
    sortedDateButton.pack(side=tk.BOTTOM, padx=5, pady=(5,5))

    searchButton = ttk.Button(ButtonFrame, text = "Search", command=lambda: SearchWindow())
    searchButton.pack(side=tk.BOTTOM, padx=5, pady=(5,5))

    column = ['Room ID', 'Guest Name', 'Guest Contact', 'Room Type', 'Price', 'Days of Stay', 'Date of Entry']
    columnWidth = [70, 180, 150, 80, 60, 80, 80]

    tree = ttk.Treeview(TableFrame, columns=column, show='headings')
    for col, width in zip(column, columnWidth):
        tree.column(col, anchor='center', width=width, minwidth=width, stretch=tk.NO)
        tree.heading(col, text=col, anchor='center')

    for room in roomList:
        tree.insert('', tk.END, values=(
            room.roomID,
            room.guestName,
            room.guestContact,
            room.roomType,
            room.Price,
            room.daysofStay,
            room.Date
        ))

    tree.pack(side=tk.LEFT, expand=True, fill='both')
    scrollbar = ttk.Scrollbar(TableFrame, orient=tk.VERTICAL, command=tree.yview)

    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def ReserveWindow():

    window = tk.Toplevel()
    window.title("Reservasi Kamar")
    global newX, newY
    window.geometry(f"220x250+{newX-245}+{newY}")

    reserveMain = RoomManager()

    inputFrame = ttk.Frame(window)
    inputFrame.pack(padx=(5, 5), pady=(10,5), expand=False, fill='both')

    tk.Label(inputFrame, text="Room ID").grid(row=0, column=0)
    roomID = tk.Entry(inputFrame)
    roomID.grid(row=0, column=1, pady=3)

    tk.Label(inputFrame, text="First Name").grid(row=1, column=0)
    firstName = tk.Entry(inputFrame)
    firstName.grid(row=1, column=1, pady=3)

    tk.Label(inputFrame, text="Last Name").grid(row=2, column=0)
    lastName = tk.Entry(inputFrame)
    lastName.grid(row=2, column=1, pady=3)

    tk.Label(inputFrame, text="Contact").grid(row=3, column=0)
    Contact = tk.Entry(inputFrame)
    Contact.grid(row=3, column=1, pady=3)

    tk.Label(inputFrame, text="Days of Stay").grid(row=4, column=0)
    daysofStay = tk.Entry(inputFrame)
    daysofStay.grid(row=4, column=1, pady=3)

    tk.Label(inputFrame, text="Date of Entry").grid(row=5, column=0)
    Date = tk.Entry(inputFrame)
    Date.grid(row=5, column=1, pady=3)
    tk.Label(inputFrame, text="*dd/mm/yy").grid(row=6, column=1, padx=(0,60))

    def confirm():
        reserveMain.roomReserve(
            roomID.get(),
            firstName.get(),
            lastName.get(),
            Contact.get(),
            int(daysofStay.get()),
            Date.get()
        )
        window.destroy()
        MainWindow()

    confirmButton = tk.Button(inputFrame, text="Confirm", command=confirm)
    confirmButton.grid( column=0, columnspan=2, pady=10, padx=(20,0))

    window.mainloop()



def RemoveWindow():
    window = tk.Toplevel()
    window.title("Reservasi Kamar")
    global newX, newY
    window.geometry(f"220x100+{newX-245}+{newY}")

    removeMain = RoomManager()

    inputFrame = ttk.Frame(window)
    inputFrame.pack(padx=(5, 5), pady=(10,5), expand=False, fill='both')

    tk.Label(inputFrame, text="Room ID").grid(row=0, column=0)
    roomID = tk.Entry(inputFrame)
    roomID.grid(row=0, column=1)

    def confirm():
        bill = removeMain.calculateBill(roomID.get())
        if bill is False:
            billNotification = "Room ID doesn't exist"
            tk.messagebox.showinfo("Bill", billNotification)
        elif bill is not None :
            billNotification = f"Total Bill: {bill}"
            tk.messagebox.showinfo("Bill", billNotification)
        elif bill is None:
            billNotification = "That Room ID isn't reserved"
            tk.messagebox.showinfo("Bill", billNotification)

        removeMain.roomRemove(roomID.get())

        window.destroy()
        MainWindow()

    confirmButton = tk.Button(inputFrame, text="Confirm", command=confirm)
    confirmButton.grid( column=0, columnspan=2, pady=20, padx=(20,0))

    window.mainloop()
    
def showContent(Room):
    tree.delete(*tree.get_children())
    for room in Room:
        tree.insert('', tk.END, values=(
            room.roomID,
            room.guestName,
            room.guestContact,
            room.roomType,
            room.Price,
            room.daysofStay,
            room.Date
        ))

def SearchWindow():
    window = tk.Toplevel()
    window.title("Reservasi Kamar")
    global newX, newY
    window.geometry(f"220x100+{newX-245}+{newY}")

    searchMain = RoomManager()

    inputFrame = ttk.Frame(window)
    inputFrame.pack(padx=(5, 5), pady=(10,5), expand=False, fill='both')

    tk.Label(inputFrame, text="Guest Name").grid(row=0, column=0)
    guestName = tk.Entry(inputFrame)
    guestName.grid(row=0, column=1)

    def search():
        keyword = guestName.get()
        result = searchMain.searchGuestName(keyword)

        if result is not None:
            MainWindow()
            global tree
            tree.delete(*tree.get_children())

            tree.insert('', tk.END, values=(
                result.roomID,
                result.guestName,
                result.guestContact,
                result.roomType,
                result.Price,
                result.daysofStay,
                result.Date
            ))
        else:
            messagebox.showinfo("Search Result", "Guest name not found.")

    searchButton = tk.Button(inputFrame, text="Search", command=search)
    searchButton.grid( column=0, columnspan=2, pady=20)

    window.mainloop()

def main():
    root.title("Hotel Management")
    global newX, newY, width, height

    root.geometry(f"{width}x{height}+{newX}+{newY}")
    root.resizable(False, False)

    root.configure(background="#4c4c6c")

    MainWindow()
    root.mainloop()

if __name__ == "__main__":
    main()
