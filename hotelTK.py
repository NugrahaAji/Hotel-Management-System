import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# global variabel -------</>
root = tk.Tk()
tree = None
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
width = 855
height = 540
newX = int((screenwidth/2)-(width/2))
newY = int((screenheight/2)-(height/2))

# membaca file .csv  -------</> 
# data.csv = roomID,Name,Contact,roomType,Price,daysofStay,Date
def csvReader():
    rooms = []
    with open('data.csv', 'r') as data:
        reader = csv.DictReader(data)
        for line in reader:
            rooms.append(line)
    return rooms

# algoritma serching -------</>
# kami sadar karena terlalu banyak menggunakan variable yang memakan banyak memori
# sehingga kami memilih BinarySearch algorithm untuk menghemat memori serta penerapannya yang tergolong mudah
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

# algoritma sorting -------</>
# kami menggunakan QuickSort karena ukuran data yang kami olah masih termasuk kedalam data kecil
# QuickSort sangat cocok serta cepat untuk mengolah data yang kecil
def quickSort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        less = [x for x in arr if key(x) < key(pivot)]
        equal = [x for x in arr if key(x) == key(pivot)]
        greater = [x for x in arr if key(x) > key(pivot)]
        return quickSort(less, key) + equal + quickSort(greater, key)



# class untuk menyimpan informasi kamar dalam sebuah list -------</>
class List:
    def __init__(self, roomID, guestName, guestContact, roomType, Price, daysofStay, Date):
        self.roomID = roomID
        self.guestName = guestName
        self.guestContact = guestContact
        self.roomType = roomType
        self.Price = Price
        self.daysofStay = daysofStay
        self.Date = Date



# class untuk mengatur informasi kamar -------</>
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
        # membaca data.csv
        reader = csvReader()
        for room in reader:
            if room['roomID'] == roomID:
                fullName = f"{firstName} {lastName}"
                room['Name'] = fullName
                room['Contact'] = contact
                room['daysofStay'] = int(daysOfStay)
                room['Date'] = date
            Update.append(room)

        # update data.csv
        with open('data.csv', 'w', newline='') as file:
            fieldnames = ['roomID', 'Name', 'Contact', 'roomType', 'Price', 'daysofStay', 'Date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(Update)
            
    def roomRemove(self, roomID):
        Update = []
        # membaca data.csv
        reader = csvReader()
        for room in reader:
            if room['roomID'] == roomID and room['Name'] != '-':
                room['Name'] = '-'
                room['Contact'] = '-'
                room['daysofStay'] = '-'
                room['Date'] = '-'
            Update.append(room)

        # update data.csv
        with open('data.csv', 'w', newline='') as file:
            fieldnames = ['roomID', 'Name', 'Contact', 'roomType', 'Price', 'daysofStay', 'Date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(Update)
            
    def calculateBill(self, roomID):
        for room in self.rooms:
            if roomID == room['roomID']:
                # jika Price dan DoS int, maka akan mengembalikan price * days
                try:
                    price = int(room['Price'])
                    days = int(room['daysofStay'])
                    return price * days
                # jika Price dan DoS bukan int, maka akan mengembalikan None
                except ValueError:
                    return None 
                
        # jika roomID tidak ditemukan, makan akan bernilai False 
        if room not in self.rooms: 
            return False
    
    def getReservedRoomID(self):
        # menyimpan kamar yang sudah dipesan
        reservedRoomID = [room.roomID for room in self.roomList if room.guestName != '-']
        return reservedRoomID
    
    def getunReservedRoomID(self):
        # menyimpan kamar yang masih kosong
        unReservedRoomID = [room.roomID for room in self.roomList if room.guestName == '-']
        return unReservedRoomID
    
    def searchGuestName(self, keyword):
        # mengubah keyword menjadi lowercase untuk menghindari case sensitive
        keyword = keyword.lower()
        keywordRoomID = binarySearch(self.roomList, keyword)
        if keywordRoomID != False:
            # jika True akan mengembalikan key roomID guest
            return self.roomList[keywordRoomID]
        else:
            # jika False akan mengembalikan None
            return None

    def sortRoomID(self):
        # memanggil function quickSort() untuk mengurutkan berdasarkan roomID
        sortedRoomID = quickSort(self.roomList, key=lambda room: room.roomID)
        return sortedRoomID
        
    def sortPrice(self):
        # memanggil function quickSort() untuk mengurutkan berdasarkan Price
        sortedPrice = quickSort(self.roomList, key=lambda room: room.Price)
        return sortedPrice



# menampilkan MainWindow -------------------------------------------------------------------------------------------</> 
def MainWindow():
    global tree
    # clear screen -------</>
    for widget in root.winfo_children():
        widget.destroy()

    # Refresh data -------</>
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
    
    # memanggil class RoomManager -------</>
    main = RoomManager()

    tk.Label(root, text="~Hotel Management", font="against 40 bold", bg="#4c4c6c", fg="#fff394").pack(side=TOP, pady= (10,0))
    # menginisialisasi fungsi menampilkan reservedRoom -------</>
    reservedRoomID = main.getReservedRoomID()
    reservedRooms = [room for room in roomList if room.roomID in reservedRoomID]
    
    # menginisialisasi fungsi menemapilkan unReservedRoom -------</>
    unReservedRoomID = main.getunReservedRoomID()
    unReservedRooms = [room for room in roomList if room.roomID in unReservedRoomID]
    
    #menginisialisasi fungsi menampilkan sortRoomID -------</>
    sortRoomID = main.sortRoomID()
    
    #menginisialisasi fungsi menampilkan sortDate -------</>
    sortPrice = main.sortPrice()

    # membuat frame tabel -------</>
    TableFrame = ttk.Frame(root)
    TableFrame.pack(side=tk.LEFT, padx=(20, 0), pady=20, expand=False, fill='both')
    
    # membuat frame Button -------</>
    ButtonFrame = ttk.Frame(root)
    ButtonFrame.pack(side=tk.RIGHT, padx = (0,20), pady=20, fill='both')
    
    # membuat button show -------</>
    RoomLabel = ttk.Label(ButtonFrame, text = 'Show Rooms', font="Montserrat 8")
    RoomLabel.pack(padx=5, pady=5)
    showAllButton = ttk.Button(ButtonFrame, text="All Rooms", command=lambda: MainWindow())
    showAllButton.pack(padx=5, pady=5)
    
    showReservedButton = ttk.Button(ButtonFrame, text="Reserved", command=lambda: showContent(reservedRooms))
    showReservedButton.pack(padx=5, pady=5)
    
    showunReservedButton = ttk.Button(ButtonFrame, text="Unreserved", command=lambda: showContent(unReservedRooms))
    showunReservedButton.pack(padx=5, pady=5)
    
    # membuat button update data -------</>
    UpdateLabel = ttk.Label(ButtonFrame, text = 'Room Update', font="Montserrat 8")
    UpdateLabel.pack(padx=5, pady=(30,0))
    reserveButton = ttk.Button(ButtonFrame, text = "Reserve", command=lambda: ReserveWindow())
    reserveButton.pack(padx=5, pady=5)
    
    removeButton = ttk.Button(ButtonFrame, text = "Remove", command=lambda: RemoveWindow())
    removeButton.pack(padx=5, pady=5)
    
    # membuat button tools -------</>
    sortRoomIDButton = ttk.Button(ButtonFrame, text="Sort by ID", command=lambda: showContent(sortRoomID))
    sortRoomIDButton.pack(side=tk.BOTTOM, padx=5, pady=(5,5))
    
    sortedDateButton = ttk.Button(ButtonFrame, text = "Sort by Price", command=lambda: showContent(sortPrice))
    sortedDateButton.pack(side=tk.BOTTOM, padx=5, pady=(5,5))
       
    searchButton = ttk.Button(ButtonFrame, text = "Search", command=lambda: SearchWindow())
    searchButton.pack(side=tk.BOTTOM, padx=5, pady=(5,5))   
    
    # membuat tabel -------</>
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
    
    # membuat scroll bar -------</>
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)



 # pop up window roomReserve ---------------------------------------------------------------------------------------</>        
def ReserveWindow():
    # membuat window pop up -------</>
    window = tk.Toplevel()
    window.title("Add Reservation")
    global newX, newY
    window.geometry(f"220x250+{newX-245}+{newY}")
    
    reserveMain = RoomManager()
    
    # membuat frame input -------</>
    inputFrame = ttk.Frame(window)
    inputFrame.pack(padx=(5, 5), pady=(10,5), expand=False, fill='both')

    # Membuat label dan entry -------</>
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
        # memanggil method roomReserve(List) -------</>
        reserveMain.roomReserve(
            roomID.get(),
            firstName.get(),
            lastName.get(),
            Contact.get(),
            int(daysofStay.get()),
            Date.get()
        )
        # menutup dan update window
        window.destroy()
        MainWindow()

    # membuat button confirm -------</>
    confirmButton = tk.Button(inputFrame, text="Confirm", command=confirm)
    confirmButton.grid( column=0, columnspan=2, pady=10, padx=(20,0))

    window.mainloop()
 
 
 
# pop up window roomRemove -----------------------------------------------------------------------------------------</>  
def RemoveWindow():
    # membuat window pop up -------</>
    window = tk.Toplevel()
    window.title("Remove Reservation")
    global newX, newY
    window.geometry(f"220x100+{newX-245}+{newY}")
    
    removeMain = RoomManager()
    
    # membuat frame input -------</>
    inputFrame = ttk.Frame(window)
    inputFrame.pack(padx=(5, 5), pady=(10,5), expand=False, fill='both')
    
    # Membuat label dan entry -------</>
    tk.Label(inputFrame, text="Room ID").grid(row=0, column=0)
    roomID = tk.Entry(inputFrame)
    roomID.grid(row=0, column=1)
    
    def confirm():
        # memanggil method calculateBill -------</>
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
            
        # memanggil method roomRemove -------</>
        removeMain.roomRemove(roomID.get())
        
        # menutup dan update window
        window.destroy()
        MainWindow()

    # membuat button confirm -------</>
    confirmButton = tk.Button(inputFrame, text="Confirm", command=confirm)
    confirmButton.grid( column=0, columnspan=2, pady=20, padx=(20,0))

    window.mainloop()
    
    
    
# pop up window searchGuestName ------------------------------------------------------------------------------------</> 
def SearchWindow():
    # membuat window pop up -------</>
    window = tk.Toplevel()
    window.title("Search Guest Name")
    global newX, newY
    window.geometry(f"220x100+{newX-245}+{newY}")
    
    searchMain = RoomManager()
        
    # membuat frame input -------</>
    inputFrame = ttk.Frame(window)
    inputFrame.pack(padx=(5, 5), pady=(10,5), expand=False, fill='both')
    
    # Membuat label dan entry -------</>
    tk.Label(inputFrame, text="Guest Name").grid(row=0, column=0)
    guestName = tk.Entry(inputFrame)
    guestName.grid(row=0, column=1)
    
    def search():
        # memanggil method searchGuestName -------</>
        keyword = guestName.get()
        result = searchMain.searchGuestName(keyword)
        
        if result is not None:
            # memanggil MainWindow -------</>
            MainWindow()  
            global tree
            # menghapus content tabel utama -------</>
            tree.delete(*tree.get_children()) 

            # menampilkan content hasil pencarian guestName -------</>
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
            
    # membuat button confirm -------</>
    searchButton = tk.Button(inputFrame, text="Search", command=search)
    searchButton.grid( column=0, columnspan=2, pady=20)

    window.mainloop()

# menampilkan content MainWindow dari fungsi pilihan ---------------------------------------------------------------</>     
def showContent(Room):
    # menghapus content tabel utama -------</>
    tree.delete(*tree.get_children())
    for room in Room:
        # menampilkan content tabel dari fungsi pilihan -------</>
        tree.insert('', tk.END, values=(
            room.roomID,
            room.guestName,
            room.guestContact,
            room.roomType,
            room.Price,
            room.daysofStay,
            room.Date
        ))

def main():
    # membuat judul window tkinter -------</>
    root.title("Hotel Management")
    global newX, newY, width, height
    
    # mengkonfigurasi ukuran layar MainWindow -------</>
    root.geometry(f"{width}x{height}+{newX}+{newY}")
    root.resizable(False, False)
    
    # kostumisasi UI MainWindow -------</>
    root.configure(background="#4c4c6c")
    
    MainWindow()
    root.mainloop()

if __name__ == "__main__":
    main()
