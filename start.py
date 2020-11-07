from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
from Main import Main1
from PIL import Image, ImageTk
from insert_staff import Registration
from change_password import ChangePassword
import os


class start:

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            query4 = "update staff set currentuser = 0 where currentuser = 1;"
            self.conn.execute(query4)
            self.conn.commit()
            self.main_root.destroy()
        else:
            return

    def login_method(self):

        c = 0
        self.query1 = "select empno from staff;"
        self.list1 = self.conn.execute(self.query1).fetchall()
        self.query2 = "select password from staff where empno="+str(self.usernameentry.get())
        self.tuple2 = self.conn.execute(self.query2).fetchone()
        self.query3 = "select authority from staff where empno="+str(self.usernameentry.get())
        self. tuple3 = self.conn.execute(self.query3).fetchone()
        authority = self.tuple3[0].split("-")
        user = self.usernameentry.get()
        for i in self.list1:

            if user == str(i[0]):
                c = 1
                if str(self.passwordentry.get()) == str(self.tuple2[0]):
                    c = 2
                    if self.adminvar.get() == 1:
                        c = 3
                        if str(authority[0]) == "admin":
                            query4 = "update staff set currentuser = 0"
                            self.conn.execute(query4)
                            query5 = "update staff set currentuser = 1 where empno=" + str(self.usernameentry.get())
                            self.conn.execute(query5)
                            self.conn.commit()
                            self.usernamevar.set("")
                            self.passwordvar.set("")
                            self.adminvar.set(0)
                            Main1(self.root, self.main_root)
                            self.root.withdraw()

                        else:
                            messagebox.showerror("School Software","You are not appoint as admin so login as staff member")
                            return
                    else:
                        c = 3
                        query4 = "update staff set currentuser = 0"
                        self.conn.execute(query4)
                        query5 = "update staff set currentuser = 1 where empno="+str(self.usernameentry.get())
                        self.conn.execute(query5)
                        self.conn.commit()
                        self.usernamevar.set("")
                        self.passwordvar.set("")
                        self.adminvar.set(0)
                        self.root.withdraw()
                        Main1(self.root,self.main_root)

        if c == 0:
            messagebox.showerror("School Software", "User not Found!Enter valid Username")
            self.usernamevar.set("")
            self.usernameentry.focus_set()

        if c == 1:
            messagebox.showerror("School Software", "Password do not match!Enter valid Password")
            self.passwordvar.set("")
            self.passwordentry.focus_set()

    def change_password_method(self):
        c = 0
        self.query1 = "select empno from staff;"
        self.list1 = self.conn.execute(self.query1).fetchall()
        self.query2 = "select password from staff where empno=" + str(self.usernameentry.get())
        self.tuple2 = self.conn.execute(self.query2).fetchone()
        user = self.usernameentry.get()
        for i in self.list1:
            if user == str(i[0]):
                c = 1
                if str(self.passwordentry.get()) == str(self.tuple2[0]):
                    c = 2
                    query1 = "update staff set currentuser=1 where empno= "+str(self.usernameentry.get())
                    self.conn.execute(query1)
                    self.conn.commit()
                    self.passwordvar.set("")
                    ChangePassword(self.root,self.main_root)
                    self.root.withdraw()

        if c == 0:
            messagebox.showerror("School Software", "User not Found!Enter valid Username")
            self.usernamevar.set("")
            self.usernameentry.focus_set()

        if c == 1:
            messagebox.showerror("School Software", "User not Found!Enter valid Password")
            self.passwordvar.set("")
            self.passwordentry.focus_set()

    def __init__(self, root, main_root):

        self.main_root = main_root
        self.root = root
        try:
            self.conn = sqlite3.connect('sinfo.db')

        except:
            messagebox.showerror("School Software", "There is some error in connection of Database")
        try:
            os.mkdir("C:\\Reports\\View\\Student")
            os.mkdir("C:\\Reports\\View\\Staff")
            os.makedirs("C:\\Reports\\LC")
            os.makedirs("C:\\Reports\\Fees")
            os.makedirs("C:\\Reports\\Salary")
            os.mkdir("C:\\Salary")
            os.makedirs("C:\\Reports\\Attendence\\Staff")
            os.makedirs("C:\\Reports\\Attendence\\Student")
            os.makedirs("C:\\Reports\\Exams")
            os.mkdir("C:\\Fees")

        except:
            pass
        rowcounter = "select count(*) from staff"
        rc = self.conn.execute(rowcounter).fetchone()
        if rc[0] == 0:
            self.root.withdraw()
            Registration(self.root, self.main_root)

        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.root.title("Start")
        self.root.config(background=self.bgclr1)
        self.root.geometry("1350x700+0+0")
        self.root.resizable(False, False)

        ##====================================================frame 1===================================================

        self.lf1 = LabelFrame(self.root, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)
        ##==================================================frame 2=====================================================
        self.lf2 = LabelFrame(self.root, text="LOG-IN WINDOW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)
        self.username = Label(self.lf2, text="Username",  bd=2, bg="black", fg="white", font=(self.f1, 15),
                              relief=GROOVE)
        self.password = Label(self.lf2, text="Password",  bd=2, bg="black", fg="white", font=(self.f1, 15),
                              relief=GROOVE)

        self.usernamevar = StringVar()
        self.usernameentry = Entry(self.lf2, textvariable=self.usernamevar, font=70)
        self.passwordvar = StringVar()
        self.passwordentry = Entry(self.lf2, textvariable=self.passwordvar, font=70, show="*")

        self.username.place(x=275, y=100)
        self.password.place(x=275, y=200)

        self.usernameentry.place(x=770, y=100)
        self.passwordentry.place(x=770, y=200)

        self.adminvar = IntVar()
        self.admin = Checkbutton(self.lf2, text="Log-in as an admin", variable=self.adminvar
                                 )
        self.admin.place(x=300, y=275)

        self.login_button = Button(self.lf2, text="Log-in", bd=5, font=(self.f2, 20), command=self.login_method)
        self.change_password_button = Button(self.lf2, text="Change Password", bd=5, font=(self.f2, 20),
                                             command=self.change_password_method)

        self.login_button.place(x=475, y=400)
        self.change_password_button.place(x=625, y=400)

        self.root.protocol("WM_DELETE_WINDOW", self.c_w)


root = Tk()
start(root, root)
root.mainloop()
