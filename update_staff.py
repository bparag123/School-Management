from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from validate_email import validate_email
from datetime import date, timedelta
from tkcalendar import DateEntry


class UpdateUser(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            query4 = "update staff set currentuser = 0 where currentuser = 1;"
            self.conn.execute(query4)
            self.conn.commit()
            self.main_root.destroy()
        else:
            return

    def update_button_method(self):
        #   """" ''' """     form  mathi  data -> database  ma  jase     """ ''' """
        try:
            a = self.firstnameentry.get().isalpha()
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
            if a:
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Last name can't be number!")
            self.lastnamevar.set("")
            return

        try:
            if (self.firstnameentry.get() == "" or self.middlenameentry.get() == "" or self.lastnameentry.get() == "" or self.salaryentry.get() == "" or self.phonenoentry.get() == "" or self.addressentry.get(1.0, END) == "\n\n" or self.emailentry.get() == "" or self.passwordentry.get() == "" or self.subjectentry.get() == "" or self.castentry.get() == ""):
                raise AttributeError
        except:
            messagebox.showerror("School Software", "Any Entry Field Can't Be Empty")
            return

        try:
            subject = self.subjectentry.get().split(",")
            for i in range(0, len(subject)):
                if not subject[i].isalpha():
                    messagebox.showerror("School Software", "Subject Entry must be numeric")
                    self.subjectentry.focus_set()
                    return

        except:
            if not self.subjectentry.get().isalpha():
                messagebox.showerror("School Software", "Subject Entry must be numeric")
                self.subjectentry.focus_set()
                return

        try:
            self.sal = int(self.salaryentry.get())
            if self.sal >= 0:
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Salary must be numeric")
            self.salaryvar.set("")
            self.salaryentry.focus_set()
            return

        try:
            self.phno = int(self.phonenoentry.get())
            if self.phno >= 0:
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Phonenember must be numeric")
            self.phonenovar.set("")
            self.phonenoentry.focus_set()
            return

        try:
            self.phno1 = list(self.phonenoentry.get())
            if len(self.phno1) != 10:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Phonenumber must be of 10-digit")
            self.phonenovar.set("")
            self.phonenoentry.focus_set()
            return

        try:
            self.phno2 = ('9', '8', '7', '6')
            if (self.phno1[0] not in self.phno2):
                raise ValueError
        except:
            messagebox.showerror("School Software", "Phonenumber must be valid")
            self.phonenovar.set("")
            self.phonenoentry.focus_set()
            return

        valid = validate_email(self.emailentry.get())
        if not valid:
            m = messagebox.showerror("Error", "email id must be valid")
            self.emailentry.focus_set()
            return

        try:
            if(self.dobentry.get_date() >= date.today()):
                raise ValueError
        except:
            messagebox.showerror("School Software","Invalid date of birth!!")
            self.dobentry.focus_set()

        try:
            if (self.categoryentry.get() == "SELECT CATEGORY"):
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please Select Category")
            self.categoryentry.focus_set()

        try:
            if (self.bloodgroupentry.get() == "SELECT BLOOD-GROUP"):
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please Select Blood-group")
            self.bloodgroupentry.focus_set()

        if self.adminvar.get() == 1:
            self.authority_value = "admin"
        else:
            self.authority_value = "staff"

        self.answer=messagebox.askyesno("School Software","Do you really want to update user whose empno="+str(self.select_user_combo.get()))

        if self.answer>0:
            query = "update staff set fname=?, mname=?, lname=?, salary=?, phno=?, address=?, email=?, authority=?, password=?, date_of_birth=?, category=?, blood_group=?, cast=? where empno=?"
            self.conn.execute(query, (self.firstnameentry.get(), self.middlenameentry.get(), self.lastnameentry.get(), self.salaryentry.get(), self.phonenoentry.get(), self.addressentry.get(1.0,END), self.emailentry.get(), self.authority_value+'-'+self.subjectentry.get(), self.passwordentry.get(), self.dobentry.get(), self.categoryentry.get(), self.bloodgroupentry.get(), self.castentry.get()))
            self.conn.commit()
            messagebox.showinfo("School Software","Operation Successful")
            self.select_user_combo.set("SELECT EMPNO")
            self.lf2.destroy()
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
        self.dobvar.set("")
        self.categoryvar.set("")
        self.bloodgroupvar.set("")
        self.castvar.set("")
        self.subjectvar.set("")
        self.dobvar.set(date.today())

    def select_combo_method(self,event=""):
        # form lakhay ne aavse.,';
        self.lf2 = LabelFrame(self, text="Update User", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=200, height=500, width=1350)

        self.firstname = Label(self.lf2, text='firstname', bd=2, bg="black", fg="white", font=(self.f1, 15),
                               relief=GROOVE)
        self.middlename = Label(self.lf2, text='middlename', bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.lastname = Label(self.lf2, text='lastname', bd=2, bg="black", fg="white", font=(self.f1, 15),
                              relief=GROOVE)
        self.salary = Label(self.lf2, text='salary', bd=2, bg="black", fg="white", font=(self.f1, 15),
                            relief=GROOVE)
        self.phoneno = Label(self.lf2, text='phoneno', bd=2, bg="black", fg="white", font=(self.f1, 15),
                             relief=GROOVE)
        self.address = Label(self.lf2, text='address', bd=2, bg="black", fg="white", font=(self.f1, 15),
                             relief=GROOVE)
        self.email = Label(self.lf2, text='email', bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)
        self.password = Label(self.lf2, text='password', bd=2, bg="black", fg="white", font=(self.f1, 15),
                              relief=GROOVE)
        self.dob = Label(self.lf2, text='DOB', bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)
        self.category = Label(self.lf2, text="Category", bd=2, bg="black", fg="white", font=(self.f1, 15),
                              relief=GROOVE)
        self.bloodgroup = Label(self.lf2, text="Blood-group", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.cast = Label(self.lf2, text="Cast", bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)
        self.subject = Label(self.lf2, text="Subjects/Post", bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)

        self.firstnamevar = StringVar()
        self.firstnameentry = Entry(self.lf2, textvariable=self.firstnamevar, font=(self.f1, 10))
        self.middlenamevar = StringVar()
        self.middlenameentry = Entry(self.lf2, textvariable=self.middlenamevar, font=(self.f1, 10))
        self.lastnamevar = StringVar()
        self.lastnameentry = Entry(self.lf2, textvariable=self.lastnamevar, font=(self.f1, 10))
        self.salaryvar = StringVar()
        self.salaryentry = Entry(self.lf2, textvariable=self.salaryvar, font=(self.f1, 10))
        self.phonenovar = StringVar()
        self.phonenoentry = Entry(self.lf2, textvariable=self.phonenovar, font=(self.f1, 10))
        self.emailvar = StringVar()
        self.emailentry = Entry(self.lf2, textvariable=self.emailvar, font=(self.f1, 10))
        self.passwordvar = StringVar()
        self.passwordentry = Entry(self.lf2, textvariable=self.passwordvar,  show="*", font=(self.f1, 10))
        self.addressentry = Text(self.lf2, width=20, height=3,wrap=WORD)
        self.dobvar = StringVar()
        self.dobentry = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                                  foreground='white', borderwidth=2, state="readonly")
        self.categoryvar = StringVar()
        self.categoryentry = ttk.Combobox(self.lf2, values=['GENERAL', 'SC', 'ST', 'OBC'], state="readonly",
                                          textvariable=self.categoryvar, font=(self.f1, 10))
        self.categoryvar.set("SELECT CATEGORY")
        self.bloodgroupvar = StringVar()
        self.bloodgroupentry = ttk.Combobox(self.lf2, values=['o+', 'o-', 'b+', 'b-', 'ab+', 'ab-'], state="readonly",
                                            textvariable=self.bloodgroupvar, font=(self.f1, 10))
        self.bloodgroupvar.set("SELECT BLOOD-GROUP")
        self.castvar = StringVar()
        self.castentry = Entry(self.lf2, textvariable=self.castvar, font=50)
        self.subjectvar = StringVar()
        self.subjectentry = Entry(self.lf2, textvariable=self.subjectvar, font=50)

        self.firstname.place(x=87.5, y=2)
        self.firstnameentry.place(x=359.37, y=2)
        self.middlename.place(x=87.5, y=52)
        self.middlenameentry.place(x=359.37, y=52)
        self.lastname.place(x=87.5, y=102)
        self.lastnameentry.place(x=359.37, y=102)
        self.salary.place(x=87.5, y=152)
        self.salaryentry.place(x=359.37, y=152)
        self.phoneno.place(x=87.5, y=202)
        self.phonenoentry.place(x=359.37, y=202)
        self.email.place(x=87.5, y=252)
        self.emailentry.place(x=359.37, y=252)
        self.password.place(x=87.5, y=302)
        self.passwordentry.place(x=359.37, y=302)
        self.address.place(x=87.5, y=352)
        self.addressentry.place(x=359.37, y=352)
        self.dob.place(x=631.25, y=2)
        self.dobentry.place(x=903.125, y=2)
        self.category.place(x=631.25, y=52)
        self.categoryentry.place(x=903.125, y=52)
        self.bloodgroup.place(x=631.25, y=102)
        self.bloodgroupentry.place(x=903.125, y=102)
        self.cast.place(x=631.25, y=152)
        self.castentry.place(x=903.125, y=152)
        self.subject.place(x=631.25, y=202)
        self.subjectentry.place(x=903.125, y=202)
        self.guide = Label(self.lf2, text="(if multiple seperate it with ',' \n for ex:maths,science)", font=(self.f1, 8))
        self.guide.place(x=903.125, y=230)
        self.guide.config(state='disabled')

        rowcounter = "select count(*) from staff;"
        rc = self.conn.execute(rowcounter).fetchone()
        self.adminvar = IntVar()
        self.admin = Checkbutton(self.lf2, text='admin', variable=self.adminvar
                                 )
        self.admin.place(x=175, y=402)
        self.authority_value = "abcd"

        self.update_query="select * from staff where empno="+str(self.select_user_combo.get())
        self.update_query_tuple = self.conn.execute(self.update_query).fetchone()

        self.firstnamevar.set(self.update_query_tuple[1])
        self.middlenamevar.set(self.update_query_tuple[2])
        self.lastnamevar.set(self.update_query_tuple[3])
        self.salaryvar.set(self.update_query_tuple[4])
        self.phonenovar.set(self.update_query_tuple[5])
        self.addressentry.insert(END,self.update_query_tuple[6])
        self.emailvar.set(self.update_query_tuple[7])

        if self.update_query_tuple[8] == 'admin':
            if rc[0] == 1:
                self.admin.config(state='disabled')
            self.adminvar.set(1)
        else:
            self.adminvar.set(0)
        self.passwordvar.set(self.update_query_tuple[10])
        self.dobvar.set(self.update_query_tuple[13])
        self.categoryvar.set(self.update_query_tuple[14])
        self.bloodgroupvar.set(self.update_query_tuple[15])
        self.castvar.set(self.update_query_tuple[16])

        self.update_button = Button(self.lf2, text="Update", command=self.update_button_method)
        self.update_button.place(x=500, y=432)

        self.reset_btn = Button(self.lf2, text="Reset",  command=self.reset)
        self.reset_btn.place(x=645, y=432)

    def __init__(self, root, main_root):
        self.main_root = main_root
        self.root = root
        try:
            self.conn = sqlite3.connect('sinfo.db')

        except:
            messagebox.showerror("School Project", "There is some error in connection of Database")
        Toplevel.__init__(self)
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.title("Update User")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)

        ##====================================================frame 1===================================================

        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)
        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 15), command=self.backf)
        bb.place(x=10, y=10, height=25)
        ##==================================================frame 2=====================================================

        query1 = "select empno from staff where currentuser=0;"
        list1 = self.conn.execute(query1).fetchall()
        my_list = []
        for i in list1:
            my_list.append(i)

        self.select_user_combo = ttk.Combobox(self, values=my_list,height=10,state="read only")
        self.select_user_combo.bind("<<ComboboxSelected>>",self.select_combo_method)
        self.select_user_combo.set("SELECT EMPNO")
        self.select_user_combo.place(x=750, y=150)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()
