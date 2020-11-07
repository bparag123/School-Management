from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from insert_student import InsertStudent
from update_student import UpdateStudent
from remove_student import RemoveStudent
from division import Division

class NewStudent(Toplevel):

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

    def insert_student_method(self):
        self.withdraw()
        InsertStudent(self,self.main_root)

    def update_student_method(self):
        self.withdraw()
        UpdateStudent(self, self.main_root)

    def remove_student_method(self):
        self.withdraw()
        RemoveStudent(self, self.main_root)

    def division(self):
        self.withdraw()
        Division(self, self.main_root)

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
        self.title("STUDENT")
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
        self.lf2 = LabelFrame(self, text="Student WINDOW", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        insert_student = Button(self.lf2, text='Insert New Student', bd=5, font=(self.f2, 15), command=self.insert_student_method)
        insert_student.place(x=200, y=200, height=30, width=250)
        update_student = Button(self.lf2,text="Update Student",  bd=5, font=(self.f2, 15), command=self.update_student_method)
        update_student.place(x=700, y=200, height=30, width=250)
        remove_student = Button(self.lf2, text="Remove Student", bd=5, font=(self.f2, 15), command=self.remove_student_method)
        remove_student.place(x=200, y=400, height=30, width=250)

        divisionButton = Button(self.lf2, text="Division", bd=5, font=(self.lf2, 15), command=self.division)
        divisionButton.place(x=700, y=400, height=30, width=250)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()