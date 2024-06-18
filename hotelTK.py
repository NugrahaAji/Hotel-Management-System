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
newX = int((screenwidth / 2) - (width / 2))
newY = int((screenheight / 2) - (height / 2))

def csvReader():
    rooms = []
    with open('data.csv', 'r') as data:
        reader = csv.DictReader(data)
        for line in reader:
            rooms.append(line)
    return rooms

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

    TableFrame = ttk.Frame(root)
    TableFrame.pack(side=tk.LEFT, padx=(20, 0), pady=20, expand=False, fill='both')

    ButtonFrame = ttk.Frame(root)
    ButtonFrame.pack(side=tk.RIGHT, padx=(0, 20), pady=20, fill='both')

    RoomLabel = ttk.Label(ButtonFrame, text='Show Rooms')
    RoomLabel.pack(padx=5, pady=5)
    showAllButton = ttk.Button(ButtonFrame, text="All Rooms")
    showAllButton.pack(padx=5, pady=5)

    showReservedButton = ttk.Button(ButtonFrame, text="Reserved")
    showReservedButton.pack(padx=5, pady=5)

    showunReservedButton = ttk.Button(ButtonFrame, text="Unreserved")
    showunReservedButton.pack(padx=5, pady=5)

    UpdateLabel = ttk.Label(ButtonFrame, text='Room Update')
    UpdateLabel.pack(padx=5, pady=(30, 0))
    reserveButton = ttk.Button(ButtonFrame, text="Reserve")
    reserveButton.pack(padx=5, pady=5)

    removeButton = ttk.Button(ButtonFrame, text="Remove")
    removeButton.pack(padx=5, pady=5)

    sortRoomIDButton = ttk.Button(ButtonFrame, text="Sort by ID")
    sortRoomIDButton.pack(side=tk.BOTTOM, padx=5, pady=(5, 5))

    sortedDateButton = ttk.Button(ButtonFrame, text="Sort by Price")
    sortedDateButton.pack(side=tk.BOTTOM, padx=5, pady=(5, 5))

    searchButton = ttk.Button(ButtonFrame, text="Search")
    searchButton.pack(side=tk.BOTTOM, padx=5, pady=(5, 5))

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