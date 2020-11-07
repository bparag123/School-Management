from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
import sqlite3
from PIL import Image, ImageTk


class RemoveStudent(Toplevel):

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

    # ========================================================to delete record============================================================

    def deleteFromTable(self, grno):
        try:
            sqliteConnection = sqlite3.connect('sinfo.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_delete = """DELETE FROM master WHERE grno=?;"""

            data_tuple = (grno)
            cursor.execute(sqlite_delete, data_tuple)
            sqliteConnection.commit()
            print("Python Variables deleted successfully from detail table")
            messagebox.showinfo('Successfully done', 'Deletion is done in database')
            cursor.close()

        except sqlite3.Error as error:
            print("delete")
            print("Failed to delete Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

# ===========================================================to check whether exam is started or not=========================================================

    def checkExam(self):

        try:
            sqliteConnection = sqlite3.connect('sinfo.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            exams = """SELECT data FROM exams;"""
            cursor.execute(exams)
            return cursor.fetchall()

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

# ========================================================Starting method============================================================

    def start(self):
        self.delete = 0
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
        self.stdchoosen = Combobox(self.lf2, state="readonly", textvariable=self.stds)
        self.stdchoosen.place(x=250, y=10, height=25, width=200)

        self.stdchoosen['values'] = self.getStd()

        self.stdchoosen.bind("<<ComboboxSelected>>", self.nextStep)

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

    # ========================================================to get gr number============================================================

    """def setValue(self):

        self.stds.set("Select Standard")
        self.rno.set("Select Roll number")
        self.grno.set("-")
        self.rollno.set("-")
        self.std.set("-")
        self.fname.set("-")
        self.mname.set("-")
        self.lname.set("-")
        self.address.set("-")
        self.phnos.set("-")
        self.phnop.set("-")
        self.email.set("-")
        self.poadd.set("-")
        self.pophno.set("-")
        self.fee.set("-")"""

    # ========================================================1st next============================================================

    def nextStep(self, event):

        if (self.stds.get() == "Select Standard"):

            messagebox.showerror('Error', 'Please select standard')

        else:

            if (self.delete != 0):
                self.clearValue()

            text = Label(self.lf2,text="Select Rollno : ",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=10, height=25)
            self.rnochoosen = Combobox(self.lf2, state="readonly", textvariable=self.rno)
            self.rnochoosen.place(x=800, y=10, height=25, width=200)
            self.rnochoosen['values'] = self.getRoll(self.stds.get(), )
            self.rnochoosen.bind("<<ComboboxSelected>>", self.nextStep2)
            # Create a Button
            """self.btn2 = Button(self.lf2, text='Next', bd='5', command=self.nextStep2)
            # Set the position of button on the top of window.
            self.btn2.place(x=100, y=550, height=25, width=150)"""

    # ========================================================2nd next============================================================

    def nextStep2(self, event):

        if (self.rno.get() == "Select Roll number"):

            messagebox.showerror('Error', 'Please select roll number')

        else:
            self.delete = 1
            self.row = self.getRow(self.stds.get(), self.rno.get())
            self.grno = (self.row[0][0])
            self.rollno = (self.row[0][1])
            self.std = (self.row[0][2])
            # self.div = (self.row[0][2].split("-")[1])
            self.fname = (self.row[0][4])
            self.mname = (self.row[0][5])
            self.lname = (self.row[0][6])
            self.address = (self.row[0][7])
            self.phnos = (self.row[0][8])
            self.phnop = (self.row[0][9])
            self.email = (self.row[0][10])
            self.poadd = (self.row[0][11])
            self.pophno = (self.row[0][12])
            self.fee = (self.row[0][13])
            self.dob = (self.row[0][16])
            self.category = (self.row[0][17])
            self.bloodg = (self.row[0][18])
            self.caste = (self.row[0][19])
            print(self.row[0][0])

            text = Label(self.lf2,text="GRno",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=50, height=25)
            self.grnotext = Label(self.lf2,text=self.grno,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.grnotext.place(x=800, y=50, height=25)

            text = Label(self.lf2,text="Rollno",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=90, height=25)
            self.rollnotext = Label(self.lf2,text=self.rollno,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.rollnotext.place(x=800, y=90, height=25)

            text = Label(self.lf2, text="Date of birth", bd=2, bg="black", fg="White", font=(self.f1, 15),
                         relief=GROOVE)
            text.place(x=550, y=290, height=25)
            self.dobtext = Label(self.lf2, text=self.dob, bd=2, bg="black", fg="White", font=(self.f1, 15),
                                    relief=GROOVE)
            self.dobtext.place(x=800, y=290, height=25)

            text = Label(self.lf2, text="Category", bd=2, bg="black", fg="White", font=(self.f1, 15),
                         relief=GROOVE)
            text.place(x=550, y=330, height=25)
            self.categorytext = Label(self.lf2, text=self.category, bd=2, bg="black", fg="White", font=(self.f1, 15),
                                    relief=GROOVE)
            self.categorytext.place(x=800, y=330, height=25)

            text = Label(self.lf2, text="Blood Group", bd=2, bg="black", fg="White", font=(self.f1, 15),
                         relief=GROOVE)
            text.place(x=550, y=370, height=25)
            self.bloodgtext = Label(self.lf2, text=self.bloodg, bd=2, bg="black", fg="White", font=(self.f1, 15),
                                    relief=GROOVE)
            self.bloodgtext.place(x=800, y=370, height=25)

            text = Label(self.lf2, text="Caste", bd=2, bg="black", fg="White", font=(self.f1, 15),
                         relief=GROOVE)
            text.place(x=550, y=410, height=25)
            self.castetext = Label(self.lf2, text=self.caste, bd=2, bg="black", fg="White", font=(self.f1, 15),
                                    relief=GROOVE)
            self.castetext.place(x=800, y=410, height=25)

            text = Label(self.lf2,text="Std.", bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=50, height=25)
            self.stdtext = Label(self.lf2, text=self.std, bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.stdtext.place(x=250, y=50, height=25)

            """text = Label(self.lf2,text="Div.")
            text.place(x=5, y=65, height=25)
            self.divtext = Label(self.lf2,text=self.div)
            self.divtext.place(x=100, y=65, height=25)"""

            text = Label(self.lf2,text="First name",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=90, height=25)
            self.fnametext = Label(self.lf2,text=self.fname,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.fnametext.place(x=250, y=90, height=25)

            text = Label(self.lf2,text="Middle name",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=130, height=25)
            self.mnametext = Label(self.lf2,text=self.mname,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.mnametext.place(x=250, y=130, height=25)

            text = Label(self.lf2,text="Last name",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=170, height=25)
            self.lnametext = Label(self.lf2,text=self.lname,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.lnametext.place(x=250, y=170, height=25)

            text = Label(self.lf2,text="Address",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=210, height=25)
            self.addresstext = Label(self.lf2,text=self.address,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.addresstext.place(x=250, y=210, height=75)

            text = Label(self.lf2,text="Phnos.",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=300, height=25)
            self.phnostext = Label(self.lf2,text=self.phnos,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.phnostext.place(x=250, y=300, height=25)

            text = Label(self.lf2,text="Phnop.",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=340, height=25)
            self.phnoptext = Label(self.lf2,text=self.phnop,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.phnoptext.place(x=250, y=340, height=25)

            text = Label(self.lf2,text="Email id",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=50, y=380, height=25)
            self.emailtext = Label(self.lf2,text=self.email,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.emailtext.place(x=250, y=380, height=25)

            text = Label(self.lf2,text="Poadd",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=130, height=25)
            self.poaddtext = Label(self.lf2,text=self.poadd,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.poaddtext.place(x=800, y=130, height=75)

            text = Label(self.lf2,text="Pophno",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=210, height=25)
            self.pophnotext = Label(self.lf2,text=self.pophno,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.pophnotext.place(x=800, y=210, height=25)

            text = Label(self.lf2,text="Fees",bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            text.place(x=550, y=250, height=25)
            self.feetext = Label(self.lf2,text=self.fee,bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
            self.feetext.place(x=800, y=250, height=25)

            # Create a Button
            self.btn3 = Button(self.lf2, text='Delete', bd='5', font=(self.f2, 15), command=self.lastStep)
            # Set the position of button on the top of window.
            self.btn3.place(x=550, y=450, height=25, width=150)

    # ========================================================Last Step============================================================

    def lastStep(self):

        self.delete = 0
        exam = self.checkExam()
        counter = 0

        try:
            for x in exam:
                if (x[0].split("_")[1].split("-")[0] == self.std.split("~")[0].split("-")[0]):
                    counter = 1
                    break
            if (counter != 1):
                pass
            else:
                raise ValueError
        except:
            messagebox.showerror("School Software", "exam is started for your standard so now you cannot leave")
            self.clearValue()
            return


        self.grn = self.getGrn(self.stds.get(), self.rno.get())
        self.deleteFromTable(self.grn[0])
        self.clearValue()

# ========================================================clear all values============================================================

    def clearValue(self):

        self.rnochoosen.destroy()
        self.grnotext.destroy()
        self.rollnotext.destroy()
        self.stdtext.destroy()
        self.fnametext.destroy()
        self.mnametext.destroy()
        self.lnametext.destroy()
        self.addresstext.destroy()
        self.phnostext.destroy()
        self.phnoptext.destroy()
        self.emailtext.destroy()
        self.poaddtext.destroy()
        self.pophnotext.destroy()
        self.feetext.destroy()
        self.dobtext.destroy()
        self.bloodgtext.destroy()
        self.categorytext.destroy()
        self.castetext.destroy()
        self.btn3.destroy()
        self.start()

    # ========================================================Main============================================================

    def __init__(self,root ,main_root):
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
        self.title("REMOVE STUDENT")
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
        self.lf2 = LabelFrame(self, text="Remove Student", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.start()

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()