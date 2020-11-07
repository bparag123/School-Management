from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
from PIL import Image, ImageTk
from validate_email import validate_email
from datetime import date


class Registration(Toplevel):
    
    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()


    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self)
        if m > 0:
            query4 = "update staff set currentuser = 0 where currentuser = 1;"
            self.conn.execute(query4)
            self.conn.commit()
            self.main_root.destroy()
        else:
            return

    def register(self):

        self.answer = messagebox.askyesnocancel("School Software","Do you really want to submit the form")

        if self.answer == True :
            print(type(self.addressentry.get(1.0,END)))
            print(self.addressentry.get(1.0,END))
            try:
                a = self.firstnameentry.get().isalpha()
                print(a)
                if a:
                    pass
                else:
                    raise ValueError
            except:
                messagebox.showerror("School Software", "First name can't be number!")
                self.firstnamevar.set("")
                return
            try:
                a = self.middlenameentry.get().isalpha()
                print(a)
                if a:
                    pass
                else:
                    raise ValueError
            except:
                messagebox.showerror("School Software", "Middle name can't be number!")
                self.middlenamevar.set("")
                return
            try:
                a = self.lastnameentry.get().isalpha()
                print(a)
                if a:
                    pass
                else:
                    raise ValueError
            except:
                messagebox.showerror("School Software", "Last name can't be number!")
                self.lastnamevar.set("")
                return
            try:
                if (self.firstnameentry.get() == "" or self.middlenameentry.get() == "" or self.lastnameentry.get() == "" or self.salaryentry.get() == "" or self.phonenoentry.get() == "" or self.addressentry.get(1.0, END) == "\n" or self.emailentry.get() == "" or self.passwordentry.get() == ""):
                    raise AttributeError
            except:
                messagebox.showerror("School Software","Any Entry Field Can't Be Empty")
                return

            try:
                self.sal = int(self.salaryentry.get())
                if self.sal >= 0:
                    pass
                else:
                    raise ValueError
            except:
                messagebox.showerror("School Software","Salary must be numeric")
                self.salaryvar.set("")
                self.salaryentry.focus_set()
                return

            try:
                self.phno = int(self.phonenoentry.get())
                if self.phno >= 0 :
                    pass
                else:
                    raise ValueError
            except:
                messagebox.showerror("School Software","Phonenember must be numeric")
                self.phonenovar.set("")
                self.phonenoentry.focus_set()
                return

            try:
                self.phno1 = list(self.phonenoentry.get())
                if len(self.phno1) != 10 :
                    raise ValueError
            except:
                messagebox.showerror("School Software","Phonenumber must be of 10-digit")
                self.phonenoentry.focus_set()
                return

            try:
                self.phno2 = ('9','8','7','6')
                if (self.phno1[0] not in self.phno2):
                    raise ValueError
            except:
                messagebox.showerror("School Software","Phonenumber must be valid")
                self.phonenoentry.focus_set()
                return

            valid = validate_email(self.emailentry.get())
            if not valid:
                m = messagebox.showerror("School Software","email id must bre valid")
                self.emailentry.focus_set()
                return

            self.command = '''insert into staff (fname,mname,lname,salary,phno,address,email,password,authority, jiondate,date_of_birth,category,blood_group,cast) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            self.conn.execute(self.command, (self.firstnameentry.get(), self.middlenameentry.get(), self.lastnameentry.get(), self.salaryentry.get(),self.phonenoentry.get(), self.addressentry.get(1.0, END), self.emailentry.get(), self.passwordentry.get(),self.authority_value, str(date.today()), self.dobentry.get(), self.categoryentry.get(), self.bloodgroupentry.get(), self.castentry.get()))
            self.conn.commit()
            self.adminvar.set(0)
            self.admin.config(state='normal')
            x = "select max(empno) from staff;"
            y = self.conn.execute(x).fetchone()
            print(y[0])
            messagebox.showinfo("School Software", str(y[0]) + " is your empno so log-in with this username")
            self.reset()
            rowcounter = "select count(*) from staff;"
            rc = self.conn.execute(rowcounter).fetchone()

            if rc[0] == 1:
                self.destroy()
                self.root.deiconify()
            else:
                return

        elif self.answer == False:
            self.reset()

        else:
            return

    def reset(self):

        self.firstnamevar.set("")
        self.firstnameentry.focus_set()
        self.middlenamevar.set("")
        self.lastnamevar.set("")
        self.salaryvar.set("")
        self.phonenovar.set("")
        self.emailvar.set("")
        self.passwordvar.set("")
        self.addressentry.delete(1.0,END)

    def __init__(self, root, main_root):

        self.main_root = main_root
        self.root = root
        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            messagebox.showerror("School Software", "Database Connection Error.")
        Toplevel.__init__(self)

        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.title("INSERT STAFF")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)
        ##===================================================frame 1====================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))

        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)
        ##=============================================frame 2==========================================================
        self.lf2 = LabelFrame(self, text="Staff Entry", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        rowcounter = "select count(*) from staff;"
        rc = self.conn.execute(rowcounter).fetchone()

        self.firstname = Label(self.lf2,text='firstname',bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.middlename = Label(self.lf2,text='middlename',bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.lastname = Label(self.lf2,text='lastname',bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.salary = Label(self.lf2,text='salary',bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.phoneno = Label(self.lf2,text='phoneno',bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.address = Label(self.lf2,text='address',bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.email = Label(self.lf2,text='email',bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.password = Label(self.lf2,text='password',bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.dob = Label(self.lf2,text='DOB',bd=2, bg="black", fg="white", font=(self.f1, 15),relief=GROOVE)
        self.category = Label(self.lf2,text="Category",bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)
        self.bloodgroup = Label(self.lf2,text="Blood-group",bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)
        self.cast = Label(self.lf2,text="Cast",bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)

        self.firstnamevar = StringVar()
        self.firstnameentry = Entry(self.lf2,textvariable = self.firstnamevar,font=50)
        self.middlenamevar = StringVar()
        self.middlenameentry = Entry(self.lf2,textvariable = self.middlenamevar,font=50)
        self.lastnamevar = StringVar()
        self.lastnameentry = Entry(self.lf2,textvariable = self.lastnamevar,font=50)
        self.salaryvar = StringVar()
        self.salaryentry = Entry(self.lf2,textvariable = self.salaryvar,font=50)
        self.phonenovar = StringVar()
        self.phonenoentry = Entry(self.lf2,textvariable = self.phonenovar,font=50)
        self.emailvar = StringVar()
        self.emailentry = Entry(self.lf2,textvariable = self.emailvar,font=50)
        self.passwordvar = StringVar()
        self.passwordentry = Entry(self.lf2, textvariable=self.passwordvar, font=50, show="*")
        self.addressentry = Text(self.lf2,width=20, height=3, font=50)
        self.dobvar = StringVar()
        self.dobentry = Entry(self.lf2,textvariable=self.dobvar,font=50)
        self.categoryvar = StringVar()
        self.categoryentry = Entry(self.lf2, textvariable=self.categoryvar, font=50)
        self.bgvar = StringVar()
        self.bloodgroupentry = Entry(self.lf2, textvariable=self.bgvar, font=50)
        self.castvar = StringVar()
        self.castentry = Entry(self.lf2, textvariable=self.castvar, font=50)

        self.firstname.place(x=87.5,y=2)
        self.firstnameentry.place(x=359.37,y=2)
        self.middlename.place(x=87.5,y=52)
        self.middlenameentry.place(x=359.37,y=52)
        self.lastname.place(x=87.5,y=102)
        self.lastnameentry.place(x=359.37,y=102)
        self.salary.place(x=87.5,y=152)
        self.salaryentry.place(x=359.37,y=152)
        self.phoneno.place(x=87.5,y=202)
        self.phonenoentry.place(x=359.37,y=202)
        self.email.place(x=87.5,y=252)
        self.emailentry.place(x=359.37,y=252)
        self.password.place(x=87.5, y=302)
        self.passwordentry.place(x=359.37, y=302)
        self.address.place(x=87.5,y=352)
        self.addressentry.place(x=359.37,y=352)
        self.dob.place(x=631.25,y=2)
        self.dobentry.place(x=903.125,y=2)
        self.category.place(x=631.25,y=52)
        self.categoryentry.place(x=903.125,y=52)
        self.bloodgroup.place(x=631.25,y=102)
        self.bloodgroupentry.place(x=903.125,y=102)
        self.cast.place(x=631.25,y=152)
        self.castentry.place(x=903.125,y=152)

        self.adminvar = IntVar()
        self.admin = Checkbutton(self.lf2, text='admin',variable=self.adminvar)
        self.admin.place(x=175, y=402)
        self.authority_value = "abcd"

        if rc[0] == 0:
            self.adminvar.set(1)
            self.admin.config(state='disabled')

        if self.adminvar.get() == 1:
            self.authority_value = "admin"
        else:
            self.authority_value = "staff"

        self.login = Button(self.lf2,text="Register",font=60,command=self.register)
        self.login.place(x=500,y=452)

        self.reset_btn = Button(self.lf2, text="Reset", font=60,command=self.reset)
        self.reset_btn.place(x=645, y=452)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()
