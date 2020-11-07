from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
import sqlite3
from tkcalendar import DateEntry
import datetime
from PIL import Image, ImageTk


class UpdateStudent(Toplevel):
    updater = 0

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

    def start(self):

        self.updater = 0
        self.stds = StringVar()
        self.stds.set("Select Standard")
        self.rno = StringVar()
        self.rno.set("Select Roll number")
        self.caste = StringVar()
        self.category = StringVar()
        self.bloodg = StringVar()
        self.dob = StringVar()
        self.grno = StringVar()
        self.rollno = StringVar()
        self.std = StringVar()
        # self.div = StringVar()
        self.fname = StringVar()
        self.mname = StringVar()
        self.lname = StringVar()
        self.address = StringVar()
        self.phnos = StringVar()
        self.phnop = StringVar()
        self.email = StringVar()
        self.poadd = StringVar()
        self.pophno = StringVar()
        self.fee = StringVar()
        print(self.stds.get())

        text = Label(self.lf2, text="Select Standard : ", bd=2, bg="black", fg="White", font=(self.f1, 15),
                     relief=GROOVE)
        text.place(x=50, y=10, height=25)
        self.stdchoosen = Combobox(self.lf2, state="readonly", textvariable=self.stds, font=(self.f1, 10))
        self.stdchoosen.place(x=250, y=10, height=25, width=200)

        self.stdchoosen['values'] = self.getStd()

        self.stdchoosen.bind("<<ComboboxSelected>>", self.nextStep)

    # ========================================================validation function============================================================

    def validNumber(self, s):
        Pattern = re.compile("(0/91)?[6-9][0-9]{9}")
        return Pattern.match(s)

    def validEmail(self, s):
        Pattern = re.compile("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")
        return Pattern.match(s)

    def validName(self, s):
        Pattern = re.compile("([A-Za-z]+)*$")
        return Pattern.match(s)

    def validRollno(self, s):
        Pattern = re.compile("^[0-9]*$")
        return Pattern.match(s)

    def validDivision(self, s):
        Pattern = re.compile("([A-Za-z]+)*$")
        return Pattern.match(s)

    def validFee(self, s):
        Pattern = re.compile("^[0-9]*$")
        return Pattern.match(s)

    # ========================================================to Update record============================================================

    def UpdateVaribleIntoTable(self, fname, mname, lname, address, phnos, phnop, email, poadd, pophno, fees, dob,
                               category, bloodg, caste, grno):
        try:
            sqliteConnection = sqlite3.connect('sinfo.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_update = """UPDATE master SET fname = ?, mname = ?, lname = ?, address = ?, student_phno = ?, parents_phno = ?, email = ?, parent_office_address = ?, parents_office_phno = ?, fee = ?, date_of_birth = ?, category = ?, blood_group = ?, cast = ? WHERE grno = ?;"""

            data_tuple = (
            fname, mname, lname, address, phnos, phnop, email, poadd, pophno, fees, dob, category, bloodg, caste, grno)
            cursor.execute(sqlite_update, data_tuple)
            sqliteConnection.commit()
            print("Python Variables Updated successfully into detail table")
            messagebox.showinfo('Successfully done', 'Entry is done in database')
            self.updater = 1
            cursor.close()

        except sqlite3.Error as error:
            print("update")
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    # ==========================================================to check validation==========================================================

    def submitvalue(self):

        self.dob = str(self.dobentry.get_date())
        self.address = self.addressentry.get(1.0, END)
        self.poadd = self.poaddentry.get(1.0, END)

        try:
            if (len(self.address) != 1):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter address")
            return

        try:
            if (len(self.poadd) != 1):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter parent office address")
            return

        """try:
            if self.category.get() != "Select Category":
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please select category")
            return"""

        try:
            if self.caste.get() != "":
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter caste")
            self.casteentry.focus_set()
            return

        """try:
            if self.dobentry.get_date() != self.today_date:
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please select date of birth")
            return"""

        """try:
            if self.bloodg.get() != "Select Blood Group":
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please select blood group")
            return"""

        """try:
            if ((self.std.get() != "") and (int(self.std.get()) >= 1) and (int(self.std.get()) <= 12)):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid standard")
            self.stdentry.focus_set()
            return"""

        try:
            if ((self.validFee(self.fee.get())) and (self.fee.get() != "")):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid fee")
            self.feesentry.focus_set()
            return

        try:
            if ((self.validName(self.fname.get())) and (self.fname.get() != "")):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid first name")
            self.fnameentry.focus_set()
            return

        try:
            if ((self.validName(self.mname.get())) and (self.mname.get() != "")):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid middle name")
            self.mnameentry.focus_set()
            return

        try:
            if ((self.validName(self.lname.get())) and (self.lname.get() != "")):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid last name")
            self.lnameentry.focus_set()
            return

        """try:
            if (self.medium.get() != "Select Medium"):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror('Error', 'please select medium but select medium after entering standard')
            return"""

        try:
            if ((self.validNumber(self.phnos.get())) and (len(self.phnos.get()) == 10)):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid student phone number")
            self.phnosentry.focus_set()
            return

        try:
            if ((self.validNumber(self.phnop.get())) and (len(self.phnop.get()) == 10)):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid parent phone number")
            self.phnopentry.focus_set()
            return

        try:
            if ((self.validNumber(self.pophno.get())) and (len(self.pophno.get()) == 10)):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid parent office phone number")
            self.pophnoentry.focus_set()
            return

        try:
            if (self.validEmail(self.email.get())):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "Please enter valid email address")
            self.emailentry.focus_set()
            return

        """if (self.validNumber(self.phnop.get()) and self.validNumber(self.phnos.get()) and self.validNumber(
                self.pophno.get()) and (len(self.phnos.get()) == 10) and (len(self.phnop.get()) == 10) and (
                len(self.pophno.get()) == 10)):

            if (self.validEmail(self.email.get())):

                if (self.validName(self.fname.get()) and self.validName(self.mname.get()) and self.validName(
                        self.lname.get()) and (self.fname.get() != "") and (self.mname.get() != "") and (
                        self.lname.get() != "")):

                    if ((self.fee.get() != "") and self.validFee(self.fee.get())):"""

        self.grn = str(self.getGrn(self.stds.get(), self.rnochoosen.get())[0][0])
        self.UpdateVaribleIntoTable(self.fname.get(), self.mname.get(), self.lname.get(), self.address,
                                    self.phnos.get(), self.phnop.get(), self.email.get(), self.poadd,
                                    self.pophno.get(), self.fee.get(), self.dob, self.category.get(), self.bloodg.get(),
                                    self.caste.get(), self.grn)
        self.setValue()
        print("done")

        """else:

                        if ((self.rno.get() == "") or (not(self.validRollno(self.rno.get())))):

                            self.rnoentry.focus_set()

                            messagebox.showinfo('Error', 'Please enter valid Roll number')


                        elif (self.div.get() == ""):

                            self.diventry.focus_set()

                            messagebox.showinfo('Error', 'Please enter Division')

                        if ((self.stds.get() == "") or (self.stds.get() < "1") or (self.stds.get() > "12")):

                            self.stdentry.focus_set()

                            messagebox.showinfo('Error', 'Please enter valid standard')

                        if ((not (self.validFee(self.fee.get()))) or (self.fee.get() == "")):
                            self.feesentry.focus_set()

                            messagebox.showinfo('Error', 'Please enter valid fees')


                else:

                    if ((not (self.validName(self.fname.get()))) or (self.fname.get() == "")):

                        self.fnameentry.focus_set()

                        messagebox.showinfo('Error', 'Invalid first name')


                    elif ((not (self.validName(self.mname.get()))) or (self.mname.get() == "")):

                        self.mnameentry.focus_set()

                        messagebox.showinfo('Error', 'Invalid middle name')


                    elif ((not (self.validName(self.lname.get()))) or (self.lname.get() == "")):

                        self.lnameentry.focus_set()

                        messagebox.showinfo('Error', 'Invalid last name')

            else:

                self.emailentry.focus_set()

                messagebox.showinfo('Error', 'Invalid email address')

        else:

            if ((not (self.validNumber(self.phnop.get()))) or (len(self.phnop.get()) != 10)):

                self.phnopentry.focus_set()
                messagebox.showinfo('Error', 'Invalid parent mobile number')

            elif ((not (self.validNumber(self.phnos.get()))) or (len(self.phnos.get()) != 10)):

                self.phnosentry.focus_set()
                messagebox.showinfo('Error', 'Invalid student mobile number')

            elif ((not (self.validNumber(self.pophno.get()))) or (len(self.pophno.get()) != 10)):

                self.pophnoentry.focus_set()
                messagebox.showinfo('Error', 'Invalid parent office mobile number')"""

    # ============================================================to set all field as null========================================================

    def setValue(self):
        self.rno = "-"
        self.std = "-"
        # self.div.set("")
        self.fname.set("")
        self.mname.set("")
        self.lname.set("")
        self.addressentry.delete(1.0, END)
        self.phnos.set("")
        self.phnop.set("")
        self.email.set("")
        self.poaddentry.delete(1.0, END)
        self.pophno.set("")
        self.fee.set("")

    # ========================================================to get standard============================================================

    def getStd(self):
        try:
            sqliteConnection = sqlite3.connect('sinfo.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_getstd = """SELECT DISTINCT standard FROM master;"""

            cursor.execute(sqlite_getstd)
            # sqliteConnection.commit()
            # print("Python Variables deleted successfully from detail table")
            # messagebox.showinfo('Successfully done', 'Deletion is done in database')
            return cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    # ========================================================to get standard============================================================

    def getRoll(self, stds, ):
        try:
            sqliteConnection = sqlite3.connect('sinfo.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_getrno = """SELECT rollno FROM master WHERE standard = ?;"""
            data_tuple = (stds,)

            cursor.execute(sqlite_getrno, data_tuple)
            # sqliteConnection.commit()
            # print("Python Variables deleted successfully from detail table")
            # messagebox.showinfo('Successfully done', 'Deletion is done in database')
            return cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    # ========================================================to get current values============================================================

    def getRow(self, stds, rno):
        try:
            sqliteConnection = sqlite3.connect('sinfo.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_getrow = """SELECT * FROM master WHERE standard = ? AND rollno = ?;"""
            data_tuple = (stds, rno)

            cursor.execute(sqlite_getrow, data_tuple)
            # sqliteConnection.commit()
            # print("Python Variables deleted successfully from detail table")
            # messagebox.showinfo('Successfully done', 'Deletion is done in database')
            return cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("roll")
            print("Failed to delete Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    # ========================================================to get gr number============================================================

    def getGrn(self, stds, rno):
        try:
            sqliteConnection = sqlite3.connect('sinfo.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_getgr = """SELECT grno FROM master WHERE standard = ? AND rollno = ?;"""
            data_tuple = (stds, rno)

            cursor.execute(sqlite_getgr, data_tuple)
            # sqliteConnection.commit()
            # print("Python Variables deleted successfully from detail table")
            # messagebox.showinfo('Successfully done', 'Deletion is done in database')
            return cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("roll")
            print("Failed to delete Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    # ========================================================1st next============================================================

    def nextStep(self, event):

        if (self.stds.get() == "Select Standard"):

            messagebox.showerror('Error', 'Please select standard')

        else:

            text = Label(self.lf2, text="Select Rollno : " ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=10, height=25)
            self.rnochoosen = Combobox(self.lf2, state="readonly", textvariable=self.rno, font=(self.f1,10))
            self.rnochoosen.place(x=800, y=10, height=25, width=200)
            self.rnochoosen['values'] = self.getRoll(self.stds.get(), )
            self.rnochoosen.bind("<<ComboboxSelected>>", self.nextStep2)
            # Create a Button
            """self.btn2 = Button(self, text='Next', bd='5', command=self.nextStep2)
            # Set the position of button on the top of window.
            self.btn2.place(x=100, y=550, height=25, width=150)"""

    # ========================================================2nd next============================================================

    def nextStep2(self, event):

        if (self.rnochoosen.get() == "Select Roll number"):

            messagebox.showerror('Error', 'Please select roll number')

        else:
            self.row = self.getRow(self.stds.get(), self.rnochoosen.get())
            self.grno = (self.row[0][0])
            self.rollno = (self.row[0][1])
            self.std = (self.row[0][2])
            # self.div = (self.row[0][2].split("-")[1])
            self.fname.set(self.row[0][4])
            self.mname.set(self.row[0][5])
            self.lname.set(self.row[0][6])
            self.address = (self.row[0][7])
            self.phnos.set(self.row[0][8])
            self.phnop.set(self.row[0][9])
            self.email.set(self.row[0][10])
            self.poadd = (self.row[0][11])
            self.pophno.set(self.row[0][12])
            self.fee.set(self.row[0][13])
            self.dob = (self.row[0][16])
            print(self.dob)
            self.category.set(self.row[0][17])
            self.bloodg.set(self.row[0][18])
            self.caste.set(self.row[0][19])
            print(self.row[0][0])

            text = Label(self.lf2,text="GRno" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=50, height=25)
            self.grnotext = Label(self.lf2,text=self.grno ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.grnotext.place(x=800, y=50, height=25)

            text = Label(self.lf2,text="Rollno" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=90, height=25)
            self.rollnotext = Label(self.lf2,text=self.rollno ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.rollnotext.place(x=800, y=90, height=25)

            text = Label(self.lf2,text="Std." ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=50, height=25)
            self.stdentry = Label(self.lf2,text=self.std ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.stdentry.place(x=250, y=50, height=25)
            self.stdentry.focus_set()

            text = Label(self.lf2,text="Date of birth" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=300, height=25)
            self.dobentry = DateEntry(self.lf2, date_pattern='yyyy/mm/dd', state="readonly", font=(self.f1,10))
            self.dobentry.place(x=800, y=300, height=25, width=150)
            self.dobentry.set_date((datetime.datetime.strptime(self.dob, "%Y-%m-%d").date()))

            text = Label(self.lf2, text="Category" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=330, height=25)
            self.categorychoosen = Combobox(self.lf2, state="readonly", textvariable=self.category, font=(self.f1,10))
            self.categorychoosen.place(x=800, y=330, height=25, width=200)

            self.categorychoosen['values'] = ["ST", "SC", "OBC", "OPEN", "Other"]

            text = Label(self.lf2, text="Blood group" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=360, height=25)
            self.bloodgchoosen = Combobox(self.lf2, state="readonly", textvariable=self.bloodg, font=(self.f1,10))
            self.bloodgchoosen.place(x=800, y=360, height=25, width=200)

            self.bloodgchoosen['values'] = ["A+", "B+", "A-", "B-", "AB+", "O+", "O-"]

            text = Label(self.lf2, text="caste" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=390, height=25)
            self.casteentry = Entry(self.lf2, textvariable=self.caste, font=(self.f1,10))
            self.casteentry.place(x=800, y=390, height=25, width=150)

            """text = Label(self.lf2,text="Div.")
            text.place(x=5, y=65, height=25)
            self.diventry = Entry(self.lf2, textvariable=self.div)
            self.diventry.place(x=100, y=65, height=25, width=150)"""

            text = Label(self.lf2,text="First name" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=90, height=25)
            self.fnameentry = Entry(self.lf2, textvariable=self.fname, font=(self.f1,10))
            self.fnameentry.place(x=250, y=90, height=25, width=150)

            text = Label(self.lf2,text="Middle name" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=130, height=25)
            self.mnameentry = Entry(self.lf2, textvariable=self.mname, font=(self.f1,10))
            self.mnameentry.place(x=250, y=130, height=25, width=150)

            text = Label(self.lf2,text="Last name" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=170, height=25)
            self.lnameentry = Entry(self.lf2, textvariable=self.lname, font=(self.f1,10))
            self.lnameentry.place(x=250, y=170, height=25, width=150)

            text = Label(self.lf2,text="Address" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=210, height=25)
            self.addressentry = Text(self.lf2, width=20, height=5, padx=2, pady=2, wrap=WORD, font=(self.f1,10))
            self.addressentry.place(x=250, y=210, height=75, width=150)
            self.addressentry.insert(INSERT, self.address)

            text = Label(self.lf2,text="Student ph." ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=300, height=25)
            self.phnosentry = Entry(self.lf2, textvariable=self.phnos, font=(self.f1,10))
            self.phnosentry.place(x=250, y=300, height=25, width=150)

            text = Label(self.lf2,text="Parent ph." ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=340, height=25)
            self.phnopentry = Entry(self.lf2, textvariable=self.phnop, font=(self.f1,10))
            self.phnopentry.place(x=250, y=340, height=25, width=150)

            text = Label(self.lf2,text="Email id" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=380, height=25)
            self.emailentry = Entry(self.lf2, textvariable=self.email, font=(self.f1,10))
            self.emailentry.place(x=250, y=380, height=25, width=150)

            text = Label(self.lf2,text="Parent office add." ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=130, height=25)
            self.poaddentry = Text(self.lf2, width=20, height=5, padx=2, pady=2, wrap=WORD, font=(self.f1,10))
            self.poaddentry.place(x=800, y=130, height=75, width=150)
            self.poaddentry.insert(INSERT, self.poadd)

            text = Label(self.lf2,text="Parent office ph." ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=220, height=25)
            self.pophnoentry = Entry(self.lf2, textvariable=self.pophno, font=(self.f1,10))
            self.pophnoentry.place(x=800, y=220, height=25, width=150)

            text = Label(self.lf2,text="Fees" ,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=260, height=25)
            self.feesentry = Entry(self.lf2, textvariable=self.fee, font=(self.f1,10))
            self.feesentry.place(x=800, y=260, height=25, width=150)

            # Create a Button
            self.btn3 = Button(self.lf2, text='Update', bd='5', font=(self.f2, 15), command=self.lastStep)
            # Set the position of button on the top of window.
            self.btn3.place(x=550, y=450, height=25, width=150)

    # ========================================================Last Step============================================================

    def lastStep(self):

        self.submitvalue()

        if (self.updater == 1):
            self.rnochoosen.destroy()
            self.grnotext.destroy()
            self.rollnotext.destroy()
            self.stdentry.destroy()
            self.fnameentry.destroy()
            self.mnameentry.destroy()
            self.lnameentry.destroy()
            self.addressentry.destroy()
            self.phnosentry.destroy()
            self.phnopentry.destroy()
            self.emailentry.destroy()
            self.poaddentry.destroy()
            self.pophnoentry.destroy()
            self.feesentry.destroy()
            self.casteentry.destroy()
            self.categorychoosen.destroy()
            self.dobentry.destroy()
            self.bloodgchoosen.destroy()
            self.btn3.destroy()
            self.start()

    # ========================================================Main============================================================

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
        self.title("UPDATE STUDENT")
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
        self.lf2 = LabelFrame(self, text="UPDATE STUDENT", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.start()



        # Create a Button
        """self.btn = Button(self, text='Next', bd='5', command=self.nextStep)
        # Set the position of button on the top of window.
        self.btn.place(x=100, y=550, height=25, width=150)"""
        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()