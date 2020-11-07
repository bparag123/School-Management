from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import json
from datetime import date, timedelta
import datetime

class Attendancestaff(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def addat(self, event=""):
        try:
            if self.cal.get_date() > date.today() :
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "You can not enter future attendance", parent=self)
            self.cal.focus_set()
            return

        year, month, day = str(self.cal.get_date()).split("-")
        date_name = datetime.date(int(year), int(month), int(day))
        day_name = date_name.strftime("%A")
        try:
            if day_name == "Sunday":
                raise ValueError
        except:
            m= messagebox.showerror("School Software", "You can not enter Sunday Attendance", parent=self)
            self.cal.focus_set()
            return

        try:
            datelimit = date.today() - timedelta(days=7)
            if datelimit > self.cal.get_date():
                raise ValueError
        except:
            m = messagebox.showerror("school software", "attendance entry date limit ", parent=self)
            self.cal.focus_set()
            return
        try:
            if self.staffbox.curselection() == ():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "Please select staff name", parent=self)
            self.staffbox.focus_set()
            return

        for item in self.staffbox.curselection():
            if self.staffinfo[item] in self.abname:
                m = messagebox.showerror("School Software", "you have alredy select '{0}' as a ansent number".format(self.staffinfo[item]), parent=self)
                return

        for item in self.staffbox.curselection():
            self.abname.append(self.staffinfo[item])
        self.attendance()
        self.submitbutton.config(state="normal")

    def rem(self, event=""):
        try:
            if self.staffbox.curselection() == ():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "Please select staff name", parent=self)
            self.staffbox.focus_set()
            return
        for item in self.staffbox.curselection():
            if self.staffinfo[item] not in self.abname:
                m = messagebox.showerror("School Software","Please mark absent then remove ", parent=self)
                return
        for item in self.staffbox.curselection():
            self.abname.remove(self.staffinfo[item])
        self.attendance()

    def submit(self, event=""):

        if self.abname == []:
            m = messagebox.showerror("School Software", "first select name  than mark absent", parent= self)
            return

        for i in self.abname:

            self.empno = i[0]
            query = """ select abdate from staff where empno=?"""
            a = self.conn.execute(query, (self.empno,)).fetchone()
            if a[0] == None:
                b = str(self.cal.get_date())
                c = list()
                c.append(b)
                p = json.dumps(c)
                query1 = """ update staff set abdate = ? where empno=?"""
                self.conn.execute(query1, (p, self.empno))
                self.conn.commit()
            else:
                x = json.loads(a[0])
                if str(self.cal.get_date()) in x:
                    messagebox.showerror("School Software ", "you alredy mark take atendane", parent=self)
                    return
                else:
                    x.append(str(self.cal.get_date()))
                p = json.dumps(x)
                query1 = """ update staff set abdate = ? where empno =?"""
                self.conn.execute(query1, (p, self.empno))
                self.conn.commit()
        m = messagebox.showinfo("School Software", "Successfuly enter absent date", parent=self)
        self.submitbutton.config(state="disabled")
        self.abname = []
        self.staffbox.focus_set()

    def attendance(self):
        self.txt.config(state="normal")
        self.txt.delete(1.0,END)
        self.txt.insert(END,"\n")
        self.txt.insert(END,"\t\t\t    Atendance")
        date = str(self.cal.get_date()).split('-')
        self.txt.insert(END,"\n\n\t\t\t Date : " + date[2] +'-'+date[1]+'-'+date[0])
        self.txt.insert(END, "\n\n\t\t\t Absent Details")
        self.txt.insert(END, "\n\n\t\t emp number\t\t\t Name")
        for item in self.abname:
            self.txt.insert(END,"\n\t\t " + str(item[0]) + "\t\t\t " + str(item[1]) + " " + str(item[2]) + " " + str(item[3]))

        self.txt.config(state="disabled")


    def __init__(self, root, main_root):

        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            m = messagebox.showerror("School Software", "Couldn't Connect With Database !", parent=self)

        self.main_root = main_root
        self.root = root
        Toplevel.__init__(self)
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"

        self.title("ATTENDANCE OF STAFF")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)

        self.abname = []

        ##====================================================frame 1===================================================

        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)

        ##==================================================frame 2=====================================================

        self.lf2 = LabelFrame(self, text="ATTENDANCE WINDOW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=675)

        self.datelabel = Label(self.lf2, text="DATE", bd=2, bg="black", fg="White", font=(self.f1, 15), relief=GROOVE)
        self.datelabel.place(x=50, y=10, height=25)

        self.cal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                             foreground='white', borderwidth=2, state="readonly")
        self.cal.place(x=300, y=10)

        self.staffnamelabel = Label(self.lf2, text="Staff Selection", bd=2, bg="black",fg='white', font=(self.f1,15),
                                    relief=GROOVE)
        self.staffnamelabel.place(x=50, y=85, height=25)

        query = """ select empno, fname, mname, lname from staff"""
        a = self.conn.execute(query).fetchall()
        self.staffinfo = []

        self.listframe = Frame(self.lf2)
        self.listframe.place(x=250, y=85, height=300, width=300)
        self.staffbox = Listbox(self.listframe, font=(self.f1, 15), selectmode="multiple", selectbackground="yellow")
        for i in a:
            self.staffinfo.append(i)
            self.staffbox.insert(END, i)
        self.staffbox.place(height=300, width=300)
        yscrollbar = Scrollbar(self.listframe)
        yscrollbar.pack(side=RIGHT, fill=Y)
        yscrollbar.config(command=self.staffbox.yview)
        xscrollbar = Scrollbar(self.listframe, orient="horizontal")
        xscrollbar.pack(side=BOTTOM, fill=X)
        xscrollbar.config(command=self.staffbox.xview)

        self.addbutton = Button(self.lf2, text="ADD", font=(self.f2, 15), bd=5, command=self.addat)
        self.addbutton.place(x=50, y=450, height=30)

        self.removebutton = Button(self.lf2, text="REMOVE", font=(self.f2, 15), bd=5, command=self.rem)
        self.removebutton.place(x=200, y=450, height=30)

        self.submitbutton = Button(self.lf2, text="SUBMIT", font=(self.f2, 15), bd=5, command=self.submit)
        self.submitbutton.place(x=350, y=450, height=30)
        self.submitbutton.config(state="disabled")

        ##==================================================frame 3=====================================================
        self.lf3 = LabelFrame(self, text="ATTENDANCE PREVIEW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf3.place(x=675, y=150, height=550, width=675)

        self.sc = Scrollbar(self.lf3)
        self.txt = Text(self.lf3, yscrollcommand=self.sc.set, borderwidth=2, relief=SUNKEN)
        self.sc.pack(side=RIGHT, fill=Y)
        self.txt.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.sc.config(command=self.txt.yview)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()