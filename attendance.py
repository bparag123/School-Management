from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import json
from datetime import date, timedelta
import datetime


class Attedance1(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def rollno(self, event=""):
        if self.rollcounter == 0:
            self.rolllabel = Label(self.lf2, text="ROLL NO", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                   relief=GROOVE)
            self.rolllabel.place(x=350, y=85, height=25)
            query1 = """ select rollno, fname, mname, lname  from master where standard = ? """
            a = self.conn.execute(query1, (self.classbox.get(),)).fetchall()
            self.rno = []
            for i in a:
                self.rno.append(i)
            self.rno.sort()
            self.frame = Frame(self.lf2)
            self.frame.place(x=350, y=150, height=100, width=100)
            self.rnobox = Listbox(self.frame, font=(self.f1, 15), selectmode="multiple", selectbackground="yellow")
            for i in self.rno:
                self.rnobox.insert(END, i[0])
            self.rnobox.pack()
            yscrollbar = Scrollbar(self.frame)
            yscrollbar.pack(side=RIGHT, fill=Y)
            yscrollbar.config(command=self.rnobox.yview)
            self.rollcounter = 1
        else:
            self.frame.destroy()
            self.rolllabel.destroy()
            self.rnobox.destroy()
            self.rollcounter = 0
            self.rollno()

    def addat(self, event=""):

        try:
            if self.cal.get_date() > date.today():
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
            m = messagebox.showerror("School Software", "You can not enter Sunday Attendance", parent=self)
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
            if(self.classbox.get() == "CLASS"):
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "First select Standard", parent=self)
            self.classbox.focus_set()
            return

        try:
            if self.rnobox.curselection() == ():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "first select roll no  than mark absent", parent= self)
            self.rnobox.focus_set()
            return

        for item in self.rnobox.curselection():
            if self.rno[item] in self.abnum:
                m = messagebox.showerror("School Software", "you have alredy select rollnumber '{0}' as a ansent number".format(self.rno[item]), parent=self)
                return

        for item in self.rnobox.curselection():
            self.abnum.append(self.rno[item])

        self.attendance()
        self.submitbutton.config(state="normal")
        self.classbox.config(state="disabled")

    def rem(self, event=""):
        try:
            if(self.classbox.get() == "CLASS"):
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "First select Standard", parent=self)
            self.classbox.focus_set()
            return
        try:
            if self.rnobox.curselection() == ():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "first select roll no  than remove absent rollnumber", parent= self)
            self.rnobox.focus_set()
            return

        for item in self.rnobox.curselection():
            if self.rno[item] not in self.abnum:
                m = messagebox.showerror("School Software","Please mark absent then remove roll number", parent=self)
                return
        for item in self.rnobox.curselection():
            self.abnum.remove(self.rno[item])
        self.attendance()

    def submit(self):

        if self.abnum == []:
            m = messagebox.showerror("School Software", "first select roll no  than mark absent", parent= self)
            return

        for item in self.abnum:

            query = """ select abday from master where standard = ? and rollno = ?"""
            a = self.conn.execute(query, (self.classbox.get(), item[0])).fetchone()
            if a[0] == None:
                b = str(self.cal.get_date())
                c = list()
                c.append(b)
                p = json.dumps(c)
                query1 = """ update master set abday = ? where standard =? and rollno=?"""
                self.conn.execute(query1, (p, self.classbox.get(), item[0]))
                self.conn.commit()
            else:
                x = json.loads(a[0])
                if str(self.cal.get_date()) in x:
                    messagebox.showerror("School Software ", "you alredy  take atendane", parent=self)
                    return
                else:
                    x.append(str(self.cal.get_date()))
                p = json.dumps(x)
                query1 = """ update master set abday = ? where standard =? and rollno=?"""
                self.conn.execute(query1, (p, self.classbox.get(), item[0]))
                self.conn.commit()
        m = messagebox.showinfo("School Software", "Successfuly enter absent date", parent=self)
        self.classbox.config(state="readonly")
        self.abnum = []
        self.submitbutton.config(state="disabled")
        self.frame.destroy()
        self.rolllabel.destroy()
        self.rnobox.destroy()
        self.classbox.set("CLASS")
        self.classbox.focus_set()

    def attendance(self):
        self.txt.config(state="normal")
        self.txt.delete(1.0, END)
        self.txt.insert(END, "\n")
        self.txt.insert(END, "\t\t\t    Atendance")
        date = str(self.cal.get_date()).split('-')
        self.txt.insert(END, "\n\n\t\t\t Date : " + date[2] + '-' + date[1] + '-' + date[0])
        self.txt.insert(END, "\n\t\t\t Standard : " + self.classbox.get())
        self.txt.insert(END, "\n\n\t\t\t Absent Details")
        self.txt.insert(END, "\n\n\t\t Roll number\t\t\t Name")
        for item in self.abnum:
            self.txt.insert(END, "\n\t\t " + str(item[0]) + "\t\t\t " + str(item[1]) + " " + str(item[2]) + " " + str(item[3]))
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

        self.title("ATTENDANCE")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)
##================================================variables ============================================================
        self.calcount = 0
        self.divcounter = 0
        self.rollcounter = 0
        self.d_ateentry = StringVar()
        self.abnum = []

##======================================================frame 1=========================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)
##=============================================frame 2==================================================================
        self.lf2 = LabelFrame(self, text="ATTENDANCE WINDOW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=675)

        self.datelabel = Label(self.lf2, text="DATE", bd=2, bg="black", fg="White", font=(self.f1, 15), relief=GROOVE)
        self.datelabel.place(x=50, y=10, height=25)

        self.cal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                    foreground='white', borderwidth=2, state="readonly")
        self.cal.place(x=300, y=10)

        self.classlabel = Label(self.lf2, text="STANDARD", bd=2, bg="black", fg="white", font=(self.f1, 15),
                            relief=GROOVE)
        self.classlabel.place(x=50, y=85, height=25)

        query = """select standard from master """
        a = self.conn.execute(query).fetchall()
        b = set(a)
        self.cals = []
        for i in b:
            self.cals.append(str(i[0]))
        self.cals.sort()

        self.c_lassbox = StringVar()
        self.classbox = ttk.Combobox(self.lf2, state="readonly", textvariable=self.c_lassbox, font=(self.f1, 10))
        self.classbox.place(x=50, y=150, height=25, width=100)
        self.classbox['values'] = self.cals
        self.classbox.bind("<<ComboboxSelected>>", self.rollno)
        self.c_lassbox.set("CLASS")

        self.addbutton = Button(self.lf2, text="ADD", font=(self.f2, 15), bd=5, command=self.addat)
        self.addbutton.place(x=50, y=450, height=30,)

        self.removebutton = Button(self.lf2, text="REMOVE", font=(self.f2, 15), bd=5, command=self.rem)
        self.removebutton.place(x=200, y=450, height=30)

        self.submitbutton = Button(self.lf2, text="SUBMIT", font=(self.f2, 15), bd=5, command=self.submit)
        self.submitbutton.place(x=400, y=450, height=30)
        self.submitbutton.config(state="disabled")

        #==============================================frame 3=========================================================
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
