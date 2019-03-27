from tkinter import *
import tkinter as tk
import calendar
import datetime
import pymysql


class Calendar:
    def __init__(self, parent):
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.day = datetime.date.today().day
        self.wid = []
        self.setup(self.year, self.month, self.day)

    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            # w.destroy()
            self.wid.remove(w)

    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        self.clear()
        self.setup(self.year, self.month, self.day)

    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
        self.clear()
        self.setup(self.year, self.month, self.day)

    def setup(self, y, m, dy):
        left = tk.Button(self.parent, text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)

        header = tk.Label(self.parent, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)

        right = tk.Button(self.parent, text='>', command=self.go_next)
        self.wid.append(right)
        right.grid(row=0, column=5)

        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3])
            self.wid.append(t)
            t.grid(row=1, column=num, columnspan=1)

        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    b = tk.Label(self.parent, width=1, text=day, background="light pink")
                    self.wid.append(b)
                    b.grid(row=w, column=d)

        today = "Today:"+str(dy)+"/"+str(m)+"/"+str(y)
        td = tk.Label(self.parent, width=2, text=today)
        self.wid.append(header)
        td.grid(row=10, column=2, columnspan=2)

        exit = tk.Button(self.parent, width=5, text='Exit', command=self.kill_and_save)
        self.wid.append(exit)
        exit.grid(row=11, column=2, columnspan=3, pady=10)

    def kill_and_save(self):
        self.parent.destroy()
        root.destroy()


name = StringVar
des = StringVar
date_time = StringVar


def add_event():
    add = Tk()
    add.title("Add Event")
    add.geometry("400x400+200+100")
    nm = Label(add, text="Event Name:")
    nm.place(x=100, y=10)
    nme = Entry(add, textvariable=name)
    nme.place(x=200, y=15)
    Label(add, text="Description:").place(x=100, y=40)
    Entry(add, textvariable=des).place(x=200, y=40)
    Label(add, text="Date-Time:").place(x=100, y=80)
    Entry(add, textvariable=date_time).place(x=200, y=80)
    Button(add, width=5, text="Add", command=add_data).place(x=250, y=160)
    add.mainloop()


def add_data():
    con = pymysql.connect("localhost", "root", "vijay", "Events")
    cur = con.cursor()
    query = 'insert into eventsall values('+str(name)+','+str(des)+','+str(date_time)+')'
    cur.execute(query)
    cur.commit()
    con.close()


root = Tk()
root.geometry("200x250+100+100")
root.title("GOOGLE CALENDAR")
rootfr = Frame(root)
rootfr.grid()
obj = Calendar(rootfr)
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Event", menu=filemenu)
filemenu.add_command(label="Add",command = add_event)
filemenu.add_command(label="Edit")
filemenu.add_command(label="Delete")
root.configure(menu=menubar)
root.mainloop()


