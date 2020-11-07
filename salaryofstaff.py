from tkinter import *
from calendar import monthrange
import sqlite3
from PIL import ImageTk, Image
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry
import json
from reportlab.pdfgen import canvas
import webbrowser
import datetime


class Salary(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def gensalary(self, event=""):

        try:
            if self.fromcal.get_date() == self.tocal.get_date():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "You cannot genrate report because both date same ",
                                     parent=self)
            self.fromcal.focus_set()
            return
        try:
            if self.tocal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "You can not gerate feture report", parent=self)
            self.tocal.focus_set()
            return
        self.cutsalary = []
        self.paysalary = []
        self.totalsalary = []
        query = """select empno, jiondate, salary, abdate,fname,mname,lname,email,phno,authority from staff"""
        self.a = self.conn.execute(query).fetchall()
        self.total_abday = []
        for item in self.a:

            self.fromdate = self.fromcal.get_date()
            self.todate = self.tocal.get_date()
            count = 0
            year, month, day = item[1].split('-')
            joindate = datetime.date(int(year), int(month), int(day))
            if joindate > self.fromcal.get_date():
                self.fromdate = joindate
            self.daygap = (self.tocal.get_date() - self.fromdate)
            self.daygap = str(self.daygap).split(' ')
            self.abdate = json.loads(item[3])
            for j in range(len(self.abdate)):
                year, month, day = self.abdate[j].split('-')
                abdate = datetime.date(int(year), int(month), int(day))
                if self.fromdate <= abdate and self.todate >= abdate:
                    count += 1
            self.total_abday.append(count)
            dailysalary = item[2] / 30
            self.cutsalary.append(dailysalary * count)
            presentday = int(self.daygap[0]) +1 - count
            self.paysalary.append(presentday * dailysalary)
            self.totalsalary.append(float(int(self.daygap[0]) + 1) * dailysalary)

        print(self.cutsalary)
        print(self.paysalary)
        print(self.totalsalary)
        self.salary_pdf()
        self.salary_report_admin()

    def salary_report_admin(self):
        pdf = canvas.Canvas("C:\\Reports\\salary\\report_{}_to_{}.pdf".format(self.fromdate, self.todate))
        pdf.setPageSize((600, 900))
        pdf.drawString(230, 880, "-: Salary Report :-")
        pdf.drawString(30, 880, "from Date : {}".format(self.fromcal.get_date()))
        pdf.drawString(450, 880, "To Date   : {}".format(self.tocal.get_date()))
        pdf.line(20, 850, 580, 850)
        pdf.line(20, 820, 580, 820)
        pdf.drawString(30, 835, "Sr No.")
        pdf.drawString(80, 835, "Emp. No.")
        pdf.drawString(150, 835, "Emp. Name")
        pdf.drawString(300, 835, "Total Salary")
        pdf.drawString(400, 835, "Cut Salary")
        pdf.drawString(500, 835, "Paid Salary")

        sr = 1
        top = 800

        for i in range(len(self.paysalary)):
            if top < 30:
                pdf.showPage()
                pdf.line(20, 850, 580, 850)
                pdf.line(20, 820, 580, 820)
                pdf.drawString(30, 835, "Sr No.")
                pdf.drawString(80, 835, "Emp. No.")
                pdf.drawString(150, 835, "Emp. Name")
                pdf.drawString(300, 835, "Total Salary")
                pdf.drawString(400, 835, "Cut Salary")
                pdf.drawString(500, 835, "Paid Salary")
                top = 800
            else:
                pdf.drawString(40, top, str(sr))
                pdf.drawString(90, top, str(self.a[i][0]))
                pdf.drawString(160, top, "{} {}".format(self.a[i][4], self.a[i][6]))
                pdf.drawString(510, top, str(round(self.paysalary[i], 2)))
                pdf.drawString(410, top, str(round(self.cutsalary[i], 2)))
                pdf.drawString(310, top, str(round(self.totalsalary[i], 2)))
                top -= 15
                sr += 1

        pdf.save()
        webbrowser.open("C:\\Reports\\salary\\staff_{}_to_{}.pdf".format(self.fromdate, self.todate))

    def salary_pdf(self):
        for i in range(len(self.a)):
            pdf = canvas.Canvas(
                "C:\\Salary\\salary_{}_{}_to_{}.pdf".format(str(self.a[i][0]), self.fromdate, self.todate))
            pdf.setPageSize((600, 450))

            pdf.line(10, 20, 590, 20)
            pdf.line(10, 430, 590, 430)
            pdf.line(20, 10, 20, 440)
            pdf.line(580, 10, 580, 440)
            pdf.line(30, 380, 570, 380)
            pdf.setFont("Courier-Bold", 20)
            pdf.drawString(220, 410, "School Name")
            pdf.setFont("Courier-Bold", 10)
            pdf.drawString(230, 370, "-: SALARY SLIP :-")
            pdf.drawString(220, 390, "Email : {}".format(str(self.a[i][7])))
            pdf.drawString(420, 390, "Phone No. : {}".format(str(self.a[i][8])))
            pdf.setFont("Courier-Bold", 10)
            pdf.drawString(30, 350, "Date :   {}".format(datetime.date.today()))
            pdf.line(70, 345, 150, 345)
            pdf.drawString(400, 350, "Receipt No :")
            pdf.line(475, 350, 520, 350)
            pdf.setFont("Courier-Bold", 13)

            pdf.drawString(30, 330,
                           "Employee Name : {} {} {}".format(str(self.a[i][4]), str(self.a[i][5]), str(self.a[i][6])))
            pdf.drawString(30, 315, "Authority : {}".format(str(self.a[i][9])))
            pdf.drawString(30, 300, "Emp. No. : {}".format(str(self.a[i][0])))

            pdf.line(30, 280, 560, 280)
            pdf.line(30, 260, 560, 260)

            pdf.drawString(340, 315, "from Date : {}".format(self.fromcal.get_date()))
            pdf.drawString(340, 300, "To Date   : {}".format(self.tocal.get_date()))

            pdf.line(30, 150, 560, 150)
            pdf.line(80, 280, 80, 150)
            pdf.drawString(30, 120, "Total Absent Days : {}".format(self.total_abday[i]))
            pdf.drawString(30, 135, "Total Salary : {}".format(round(self.totalsalary[i], 2)))
            pdf.drawString(30, 105, "Salary Deduction : {}".format(round(self.cutsalary[i], 2)))
            pdf.drawString(30, 270, "Sr No.")
            pdf.drawString(160, 270, "Details")
            pdf.drawString(400, 270, "Paid Amount")
            pdf.drawString(50, 230, "1")
            pdf.drawString(160, 230, "Salary")
            pdf.line(300, 280, 300, 150)
            pdf.drawString(400, 230, str(round(self.paysalary[i], 2)))
            pdf.drawString(480, 50, "Signature")
            pdf.drawString(478, 35, "(Receiver)")
            pdf.line(470, 65, 565, 65)
            pdf.save()
            webbrowser.open("C:\\Salary\\salary_{}_{}_to_{}.pdf".format(str(self.a[i][0]), self.fromdate, self.todate))

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
        self.title("SALARY")
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
        self.lf2 = LabelFrame(self, text="Salary", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.fromdatelabel = Label(self.lf2, text="FROM DATE", bd=2, bg="black", fg="White", font=(self.f1, 15),
                                   relief=GROOVE)
        self.fromdatelabel.place(x=50, y=10, height=25)

        self.fromcal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                                 foreground='white', borderwidth=2, state="readonly")
        self.fromcal.place(x=250, y=10, height=25)

        self.todatelabel = Label(self.lf2, text="TO DATE", bd=2, bg="black", fg="White", font=(self.f1, 15),
                                 relief=GROOVE)
        self.todatelabel.place(x=550, y=10, height=25)

        self.tocal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                               foreground='white', borderwidth=2, state="readonly")
        self.tocal.place(x=750, y=10, height=25)

        self.salarybutton = Button(self.lf2, text="Genrate Salary", bd=5, font=(self.f2, 15), command=self.gensalary)
        self.salarybutton.place(x=550, y=450, height=30)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()