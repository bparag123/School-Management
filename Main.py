from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from new_exam import r1
from attendance import Attedance1
from fee import fee1
from staff import NewUser
from student import NewStudent
from reports import Reports

class Main1(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def at(self, event=""):
        self.withdraw()
        Attedance1(self, self.main_root)

    def fee(self,event=""):
        self.withdraw()
        fee1(self, self.main_root)

    def sinfo(self, event=""):
        self.withdraw()
        NewStudent(self,self.main_root)

    def result(self, event=""):
        self.withdraw()
        r1(self, self.main_root)

    def re(self, event=""):
        self.withdraw()
        Reports(self, self.main_root)

    def stinfo(self, event=""):
        query = "select authority from staff where currentuser=1;"
        self.authority = self.conn.execute(query).fetchone()
        if self.authority[0] == "admin":
            self.withdraw()
            NewUser(self, self.main_root)
        else:
            messagebox.showerror("School Software", "You are not appoint as admin so you can't handle staff info")
            return

    def __init__(self, root, main_root):

        self.main_root = main_root
        self.root = root
        try:
            self.conn = sqlite3.connect('sinfo.db')

        except:
            messagebox.showerror("School Software", "There is some error in connection of Database")
        Toplevel.__init__(self)
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.title("MAIN")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)
        ##===================================================frame1 ====================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), bg="white", command=self.backf)
        bb.place(x=10, y=10)
        ##===============================================frame 2========================================================
        self.lf2 = LabelFrame(self, text="Buttons", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        atimg = ImageTk.PhotoImage(file="attendance.png")
        atbutton = Button(self.lf2, image=atimg, bd=5, bg=self.bgclr2, relief=FLAT, command=self.at)
        atbutton.place(x=50, y=50, height=175, width=350)

        feeimg = ImageTk.PhotoImage(file="fee.jpeg")
        feebutton = Button(self.lf2, image=feeimg, bd=5, bg=self.bgclr2, relief=FLAT, command=self.fee)
        feebutton.place(x=500, y=50, height=175, width=350)

        simg = ImageTk.PhotoImage(file="student.jpg")
        sbutoon = Button(self.lf2, image=simg, bd=5, bg=self.bgclr2, relief=FLAT, command=self.sinfo)
        sbutoon.place(x=950, y=50, height=175, width=350)

        rimg = ImageTk.PhotoImage(file="exam.jpg")
        rbutton = Button(self.lf2, image=rimg, bd=5, bg=self.bgclr2, relief=FLAT, command=self.result)
        rbutton.place(x=50, y=300, height=175, width=350)

        reimg = ImageTk.PhotoImage(file="report.jpg")
        rebutton = Button(self.lf2, image=reimg, bd=5, bg=self.bgclr2, relief=FLAT, command=self.re)
        rebutton.place(x=500, y=300, height=175, width=350)

        stimg = ImageTk.PhotoImage(file="staff.png")
        stbutton = Button(self.lf2, image=stimg, bd=5, bg=self.bgclr2, relief=FLAT, command=self.stinfo)
        stbutton.place(x=950, y=300, height=175, width=350)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()