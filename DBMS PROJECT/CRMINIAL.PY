import sqlite3
from tkinter import *
from tkinter import messagebox


class CRIMINAL1:
    def __init__(self):
        self.conn = sqlite3.connect("criminal_database.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS CRIMINAL(CRIMINAL_ID INTEGER PRIMARY KEY, CRIMINAL_NAME TEXT, DOCUMENT TEXT, CRIMINAL_PHONE_NO INTEGER, STREET_NAME TEXT, CITY TEXT, PINCODE INTEGER)"
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM CRIMINAL")
        rows = self.cur.fetchall()
        return rows

    def insert(
        self, CRIMINAL_NAME, DOCUMENT, CRIMINAL_PHONE_NO, STREET_NAME, CITY, PINCODE
    ):
        self.cur.execute(
            "INSERT INTO CRIMINAL VALUES (NULL,?,?,?,?,?,?)",
            (CRIMINAL_NAME, DOCUMENT, CRIMINAL_PHONE_NO, STREET_NAME, CITY, PINCODE),
        )
        self.conn.commit()
        self.view()

    def update(
        self,
        CRIMINAL_ID,
        CRIMINAL_NAME,
        DOCUMENT,
        CRIMINAL_PHONE_NO,
        STREET_NAME,
        CITY,
        PINCODE,
    ):
        self.cur.execute(
            "UPDATE CRIMINAL SET CRIMINAL_NAME=?, DOCUMENT=?, CRIMINAL_PHONE_NO=?, STREET_NAME=?, CITY=?, PINCODE=? WHERE CRIMINAL_ID=?",
            (
                CRIMINAL_NAME,
                DOCUMENT,
                CRIMINAL_PHONE_NO,
                STREET_NAME,
                CITY,
                PINCODE,
                CRIMINAL_ID,
            ),
        )
        self.view()

    def delete(self, CRIMINAL_ID):
        self.cur.execute("DELETE FROM CRIMINAL WHERE CRIMINAL_ID=?", (CRIMINAL_ID,))
        self.conn.commit()
        self.view()


db = CRIMINAL1()


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
    e4.delete(0, END)
    e4.insert(END, selected_tuple[4])
    e5.delete(0, END)
    e5.insert(END, selected_tuple[5])
    e6.delete(0, END)
    e6.insert(END, selected_tuple[6])


def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)


def add_command():
    db.insert(
        CRIMINAL_NAME_text.get(),
        DOCUMENT_text.get(),
        CRIMINAL_PHONE_NO_text.get(),
        STREET_NAME_text.get(),
        CITY_text.get(),
        PINCODE_text.get(),
    )
    list1.delete(0, END)
    list1.insert(
        END,
        (
            CRIMINAL_NAME_text.get(),
            DOCUMENT_text.get(),
            CRIMINAL_PHONE_NO_text.get(),
            STREET_NAME_text.get(),
            CITY_text.get(),
            PINCODE_text.get(),
        ),
    )


def delete_command():
    db.delete(selected_tuple[0])


def update_command():
    db.update(
        selected_tuple[0],
        CRIMINAL_NAME_text.get(),
        DOCUMENT_text.get(),
        CRIMINAL_PHONE_NO_text.get(),
        STREET_NAME_text.get(),
        CITY_text.get(),
        PINCODE_text.get(),
    )


window = Tk()

window.title("CRIMINAL")


def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        del dd


window.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing

l1 = Label(window, text="CRIMINAL NAME")
l1.grid(row=0, column=0)

l2 = Label(window, text="DOCUMENT")
l2.grid(row=1, column=0)

l3 = Label(window, text="CRIMINAL PHONE NO")
l3.grid(row=2, column=0)

l4 = Label(window, text="STREET NAME")
l4.grid(row=3, column=0)

l5 = Label(window, text="CITY")
l5.grid(row=4, column=0)

l6 = Label(window, text="PINCODE")
l6.grid(row=5, column=0)

CRIMINAL_NAME_text = StringVar()
e1 = Entry(window, textvariable=CRIMINAL_NAME_text)
e1.grid(row=0, column=1)

DOCUMENT_text = StringVar()
e2 = Entry(window, textvariable=DOCUMENT_text)
e2.grid(row=1, column=1)

CRIMINAL_PHONE_NO_text = StringVar()
e3 = Entry(window, textvariable=CRIMINAL_PHONE_NO_text)
e3.grid(row=2, column=1)

STREET_NAME_text = StringVar()
e4 = Entry(window, textvariable=STREET_NAME_text)
e4.grid(row=3, column=1)

CITY_text = StringVar()
e5 = Entry(window, textvariable=CITY_text)
e5.grid(row=4, column=1)

PINCODE_text = StringVar()
e6 = Entry(window, textvariable=PINCODE_text)
e6.grid(row=5, column=1)

list1 = Listbox(window, height=6, width=42)
list1.grid(row=8, column=0, rowspan=8, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=9, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind("<<ListboxSelect>>", get_selected_row)

b1 = Button(window, text="DISPLAY TABLE", width=15, command=view_command)
b1.grid(row=8, column=3)

b3 = Button(window, text="INSERT ", width=15, command=add_command)
b3.grid(row=9, column=3)

b4 = Button(window, text="UPDATE", width=15, command=update_command)
b4.grid(row=10, column=3)

b5 = Button(window, text="DELETE", width=15, command=delete_command)
b5.grid(row=11, column=3)

window.mainloop()
