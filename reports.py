from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from remaining_fee import Remaining_fee
from student_attendance_report import StudentAttendanceReport
from staff_standance_report import Staffatreport
from view_student import ViewStudent
from view_staff import ViewStaff


class Reports(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def stud_atten_report_method(self):
        self.withdraw()
        StudentAttendanceReport(self,self.main_root)

    def atreport(self,event=""):
        self.withdraw()
        Staffatreport(self, self.main_root)

    def student_view_report(self):
        self.withdraw()
        ViewStudent(self,self.main_root)

    def staff_view_report(self):
        self.withdraw()
        ViewStaff(self,self.main_root)

    def remaining_fee(self):
        self.withdraw()
        Remaining_fee(self, self.main_root)

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
        self.title("REPORTS")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)

        ##===============================================frame 1========================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)
        ##=============================================frame 2==========================================================
        self.lf2 = LabelFrame(self, text="REPORT'S", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.stud_atten_report_btn = Button(self.lf2, text="Student Attendance Report", bd=5, font=(self.f1, 15), bg=self.bgclr2, command=self.stud_atten_report_method)
        self.stud_atten_report_btn.place(x=200,y=100)

        self.staffat_report_btn = Button(self.lf2, text="Staff Attedance Report", bd=5, font=(self.f1, 15), bg=self.bgclr2, command=self.atreport)
        self.staffat_report_btn.place(x=200,y=250)

        self.student_view = Button(self.lf2, text="View Student", bd=5, font=(self.f1, 15), bg=self.bgclr2, command=self.student_view_report)
        self.student_view.place(x=800,y=175)

        self.fee_gen_btn = Button(self.lf2, text="Remaining Fee Report", bd=5, font=(self.f1, 15), bg=self.bgclr2,command=self.remaining_fee)
        self.fee_gen_btn.place(x=200, y=400)

        query = "select authority from staff where currentuser=1;"
        self.authority = self.conn.execute(query).fetchone()
        if self.authority[0] == "admin":
            self.staff_view = Button(self.lf2, text="View Staff", bd=5, font=(self.f1, 15), bg=self.bgclr2,command=self.staff_view_report)
            self.staff_view.place(x=800, y=325)

        self.protocol("WM_DELETE_WINDOW", self.c_w)

        self.mainloop()