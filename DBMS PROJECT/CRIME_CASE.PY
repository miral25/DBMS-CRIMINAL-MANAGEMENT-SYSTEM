import sqlite3
from tkinter import *
from tkinter import messagebox

class CRIME_CASE1:
    def __init__(self):
        self.conn = sqlite3.connect("criminal_database.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS CRIME_CASE (C_ID INTEGER PRIMARY KEY, CRIME_DESCRIPTION TEXT, LOCATION TEXT, SUSPECT TEXT)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM CRIME_CASE")
        rows = self.cur.fetchall()
        return rows

    def insert(self, CRIME_DESCRIPTION, LOCATION, SUSPECT):
        self.cur.execute("INSERT INTO CRIME_CASE VALUES (NULL,?,?,?)", (CRIME_DESCRIPTION, LOCATION, SUSPECT))
        self.conn.commit()
        self.view()

    def update(self, C_ID, CRIME_DESCRIPTION, LOCATION, SUSPECT):
        self.cur.execute("UPDATE CRIME_CASE SET CRIME_DESCRIPTION=?, LOCATION=?, SUSPECT=? WHERE C_ID=?", (CRIME_DESCRIPTION, LOCATION, SUSPECT, C_ID))
        self.view()

    def delete(self, C_ID):
        self.cur.execute("DELETE FROM CRIME_CASE WHERE C_ID=?", (C_ID,))
        self.conn.commit()
        self.view()

db = CRIME_CASE1()


def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])


def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)

def add_command():
    db.insert(CRIME_DESCRIPTION_text.get(), LOCATION_text.get(), SUSPECT_text.get())
    list1.delete(0, END)
    list1.insert(END, (CRIME_DESCRIPTION_text.get(), LOCATION_text.get(), SUSPECT_text.get()))


def delete_command():
    db.delete(selected_tuple[0])


def update_command():
    db.update(selected_tuple[0], CRIME_DESCRIPTION_text.get(), LOCATION_text.get(), SUSPECT_text.get())


window = Tk()

window.title("CRIME_CASE")

def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        del dd


window.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing

l1 = Label(window, text="CRIME_DESCRIPTION")
l1.grid(row=0, column=0)

l2 = Label(window, text="LOCATION")
l2.grid(row=1, column=0)

l3 = Label(window, text="SUSPECT")
l3.grid(row=2, column=0)

CRIME_DESCRIPTION_text = StringVar()
e1 = Entry(window, textvariable=CRIME_DESCRIPTION_text)
e1.grid(row=0, column=1)

LOCATION_text = StringVar()
e2 = Entry(window, textvariable=LOCATION_text)
e2.grid(row=1, column=1)

SUSPECT_text = StringVar()
e3 = Entry(window, textvariable=SUSPECT_text)
e3.grid(row=2, column=1)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=5, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=5, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command = list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text="DISPLAY TABLE", width = 15, command = view_command)
b1.grid(row=5, column=3)

b3 = Button(window, text="INSERT ", width = 15, command = add_command)
b3.grid(row=6, column=3)

b4 = Button(window, text="UPDATE", width = 15, command = update_command)
b4.grid(row=7, column=3)

b5 = Button(window, text="DELETE", width = 15, command = delete_command)
b5.grid(row=8, column=3)

window.mainloop()