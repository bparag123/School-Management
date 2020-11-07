from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from updatedivision import Updatedivision

class Division(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def updatediv(self,event=""):
        self.withdraw()
        Updatedivision(self, self.main_root)

    def rollno(self, event=""):

        if self.rollcounter == 0:
            self.rolllabel = Label(self.lf2, text="Student's", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                   relief=GROOVE)
            self.rolllabel.place(x=350, y=85, height=25)
            query1 = """ select rollno, fname, mname, lname  from master where standard = ? """
            a = self.conn.execute(query1, (self.classbox.get(),)).fetchall()
            self.rno = []
            for i in a:
                self.rno.append(i)
            self.rno.sort()
            self.frame = Frame(self.lf2)
            self.frame.place(x=350, y=150, height=300, width=400)
            self.rnobox = Listbox(self.frame, font=(self.f1, 15), selectmode="multiple", selectbackground="yellow")
            for i in self.rno:
                self.rnobox.insert(END, i)
            self.rnobox.place(height=300,width=400)
            yscrollbar = Scrollbar(self.frame)
            yscrollbar.pack(side=RIGHT, fill=Y)
            yscrollbar.config(command=self.rnobox.yview)
            xscrollbar = Scrollbar(self.frame, orient="horizontal")
            xscrollbar.pack(side=BOTTOM, fill=X)
            xscrollbar.config(command=self.rnobox.xview)
            self.rollcounter = 1
        else:
            self.frame.destroy()
            self.rolllabel.destroy()
            self.rnobox.destroy()
            self.rollcounter = 0
            self.rollno()

    def add(self, event=""):

        try:
            if(self.classbox.get() == "CLASS"):
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "please select standard", parent=self)
            self.classbox.focus_set()
            return
        try:
            if(self.diventry.get() == ""):
                raise ValueError
        except:
            m = messagebox.showerror("School Software","Please enter division name", parent=self)
            self.diventry.focus_set()
            return
        try:
            if( not self.diventry.get().isalpha() ):
                raise ValueError
            if(len(self.diventry.get()) != 1):
                raise ValueError
        except:
            m = messagebox.showerror("school software", "division name must be in single character ", parent=self)
            self.diventry.focus_set()
            return
        try:
            query2 = """ select standard from master"""
            a = self.conn.execute(query2).fetchall()
            b = set(a)
            self.updatecals = []
            for i in b:
                if (str(i[0])):
                    self.updatecals.append(i[0])
            self.updatestd = self.classbox.get() +"-"+ self.diventry.get()
            if self.updatestd in self.updatecals:
                raise ValueError
        except:
            m = messagebox.showerror("School Software","Division name alredy exits", parent=self)
            self.diventry.focus_set()
            return

        query = """ update master set standard = ?, div = ? where rollno=? and standard = ?"""
        y = self.rnobox.curselection()
        for item in y:
            self.rollnumber = self.rno[item]
            self.conn.execute(query,(self.updatestd, 1 ,self.rollnumber[0], self.classbox.get()))
        self.d_iventry.set("")
        self.rollno()
        query1 = """select rollno from master where standard=?"""
        x = self.conn.execute(query1,(self.classbox.get(),)).fetchall()
        if x != []:
            self.classbox.config(state="disabled")
            self.divisionbutton.config(state="disabled")
        else:
            self.divisionbutton.config(state="normal")

    def division(self, event=""):
        m = messagebox.askyesnocancel("School Software","Are you want save changes", parent=self)
        if m == True:
            self.conn.commit()
            self.destroy()
            Division(self.root, self.main_root)
        elif m == False:
            self.conn.rollback()
            self.destroy()
            Division(self.root, self.main_root)
        elif m == None:
            return

    def __init__(self, root, main_root):

        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            m = messagebox.showerror("School Software","Couldn't Connect With Database !", parent=self)

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
        self.title("Division")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)

        self.rollcounter = 0

        ##======================================================frame 1=================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)

        ##====================================================frame 2===================================================

        self.lf2 = LabelFrame(self, text="Division", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.classlabel = Label(self.lf2, text="STANDARD", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.classlabel.place(x=50, y=85, height=25)

        query = """select standard from master """
        a = self.conn.execute(query).fetchall()
        b = set(a)
        self.cals = []
        for i in b:
            if("-" not in str(i[0])):
                self.cals.append(i[0])

        self.c_lassbox = StringVar()
        self.classbox = ttk.Combobox(self.lf2, state="readonly", textvariable=self.c_lassbox, font=(self.f1, 10))
        self.classbox.place(x=50, y=150, height=25)
        self.classbox['values'] = self.cals
        self.classbox.bind("<<ComboboxSelected>>", self.rollno)
        self.c_lassbox.set("CLASS")

        self.divlabel = Label(self.lf2, text="DIVISION", bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)
        self.divlabel.place(x=50, y=225, height=25)

        self.d_iventry = StringVar()
        self.diventry = Entry(self.lf2, textvariable=self.d_iventry, font=(self.f1, 15))
        self.diventry.place(x=50, y=300, height=25, width=100)
        self.divisionbutton = Button(self.lf2, text="Create Division", bd=5, font=(self.f2, 15), command=self.division)
        self.divisionbutton.place(x=1000, y=225, height=25)
        self.divisionbutton.config(state="disabled")

        self.updatedivbutton = Button(self.lf2, text="Update Division", bd=5, font=(self.f2, 15), command=self.updatediv)
        self.updatedivbutton.place(x=1000, y=350, height=25)

        self.addbutton = Button(self.lf2, text="ADD", bd=5, font=(self.f2, 15), command=self.add)
        self.addbutton.place(x=1000, y=100, height=25)

        self.protocol("WM_DELETE_WINDOW", self.c_w)

        self.mainloop()

