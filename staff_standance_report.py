from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import json
from datetime import date, timedelta
from reportlab.pdfgen import canvas
import webbrowser


class Staffatreport(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def atreport(self, event=""):

        try:
            if self.fromcal.get_date() == self.tocal.get_date():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "You cannot genrate report because both date same ", parent=self)
            self.fromcal.focus_set()
            return
        try:
            if self.fromcal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You can not genrate feature report", parent=self)
            self.fromcal.focus_set()
            return
        try:
            if self.tocal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You can not gerate feture report", parent=self)
            self.tocal.focus_set()
            return

        query = """ select abdate from staff """
        a = self.conn.execute(query).fetchall()
        self.abdate_all = []
        for item in a:
            if item[0] != None:
                fetched_list = json.loads(item[0])
                self.abdate_all.append(fetched_list)
        self.staff_pdf_report_all()

    def spreport(self, event=""):

        try:
            if self.fromcal.get_date() == self.tocal.get_date():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "You cannot genrate report because both date same ", parent=self)
            self.fromcal.focus_set()
            return
        try:
            if self.fromcal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You can not genrate feature report", parent=self)
            self.fromcal.focus_set()
            return
        try:
            if self.tocal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You can not genrate feature report", parent=self)
            self.tocal.focus_set()

        y = self.staffbox.curselection()
        if y == ():
            m = messagebox.showerror("School Software","Please select any staff member", parent=self)
            self.staffbox.focus_set()
            return
        else:
            self.empno = self.staffinfo[y[0]]
            query = """ select abdate from staff where empno= ? """
            a = self.conn.execute(query, (self.empno[0], )).fetchone()
            print(type(a[0]))
            self.abdate = json.loads(a[0])
            self.staff_pdf_report()

    def staff_pdf_report_all(self):
        pdf = canvas.Canvas("C:\\Reports\\Attendence\\Staff\\report_all_{}_to_{}.pdf".format(self.fromcal.get_date(), self.tocal.get_date()))
        pdf.setPageSize((600, 900))
        pdf.setFont("Courier-Bold", 20)
        pdf.drawString(200, 880, "Attendence Report")
        pdf.setFont("Courier-Bold", 15)
        pdf.drawString(30, 815, "Emp. no ")
        pdf.drawString(300, 815, "Absent Dates")
        pdf.drawString(30, 860, "From Date : {}".format(self.fromcal.get_date()))
        pdf.drawString(350, 860, "To Date : {}".format(self.tocal.get_date()))
        pdf.line(30, 800, 580, 800)
        pdf.line(30, 830, 580, 830)
        top = 760
        line = False
        total_length = len(self.abdate_all)
        for i in range(total_length):
            x = len(self.abdate_all[i])
            for j in range(x):
                if top < 30:
                    pdf.showPage()
                    top = 830
                    pdf.setFont("Courier-Bold", 15)
                    pdf.drawString(30, 865, "Emp. no ")
                    pdf.drawString(300, 865, "Absent Dates")
                    pdf.line(30, 880, 580, 880)
                    pdf.line(30, 860, 580, 860)
                if j == 0:
                    emp = "{}-{}".format(self.staffinfo[i][0], self.staffinfo[i][1])
                    pdf.drawString(50, top, emp)
                if str(self.fromcal.get_date()) <= str(self.abdate_all[i][j]) and str(self.tocal.get_date()) >= str(self.abdate_all[i][j]):
                    line = True
                    pdf.drawString(320, top, str(self.abdate_all[i][j]))
                    top -= 200
            if line:
                pdf.line(50, top , 560 ,top)
                top -= 200

        print("Successful")
        pdf.save()
        webbrowser.open("C:\\Reports\\Attendence\\Staff\\report_all_{}_to_{}.pdf".format(self.fromcal.get_date(), self.tocal.get_date()))

    def staff_pdf_report(self):

        pdf = canvas.Canvas("C:\\Reports\\Attendence\\Staff\\report_{}_{}_to_{}.pdf".format(self.empno[0], self.fromcal.get_date(), self.tocal.get_date()))
        pdf.setPageSize((600, 900))
        pdf.line(10, 700, 590, 700)
        pdf.line(10, 860, 590, 860)
        pdf.line(20, 690, 20, 870)
        pdf.line(580, 690, 580, 870)
        pdf.setFont("Courier-Bold", 20)
        pdf.drawString(200, 880, "Attendence Report")
        pdf.setFont("Courier-Bold", 15)
        pdf.drawString(30, 840, "Employee Name : {} {} {}".format(self.empno[1], self.empno[2], self.empno[3]))
        pdf.drawString(30, 815, "Emp. no : ".format(self.empno[0]))
        pdf.drawString(50, 650, "Sr. No")
        pdf.drawString(300, 650, "Absent Dates")
        pdf.drawString(30, 790, "From Date : {}".format(self.fromcal.get_date()))
        pdf.drawString(30, 765, "To Date : {}".format(self.tocal.get_date()))
        sr = 1
        side_sr = 55
        side_date = 320
        top = 600
        print(type(self.fromcal.get_date()))
        for i in self.abdate:
            if top<30:
                pdf.showPage()
                top = 800
            else:
                if str(self.fromcal.get_date()) <= i and str(self.tocal.get_date()) >= i:
                    pdf.drawString(side_sr, top, str(sr))
                    pdf.drawString(side_date, top, str(i))
                    top -= 15
                    sr += 1

        pdf.save()
        print("succesfull")
        webbrowser.open("C:\\Reports\\Attendence\\Staff\\report_{}_{}_to_{}.pdf".format(self.empno[0], self.fromcal.get_date(), self.tocal.get_date()))

    def __init__(self, root, main_root):

        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            m = messagebox.showerror("School Software", "Couldn't Connect With Database !", parent=self)

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
        self.title("STAFF ATTENDANCE REPORT")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)

        ##====================================================frame 1===================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)

        ##==================================================frame 2=====================================================

        self.lf2 = LabelFrame(self, text="ATTENDANCE WINDOW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.fromdatelabel = Label(self.lf2, text="FROM DATE", bd=2, bg="black", fg="White", font=(self.f1, 15), relief=GROOVE)
        self.fromdatelabel.place(x=50, y=10, height=25)

        self.fromcal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                             foreground='white', borderwidth=2, state="readonly")
        self.fromcal.place(x=250, y=10, height=25)

        self.todatelabel = Label(self.lf2, text="TO DATE", bd=2, bg="black", fg="White", font=(self.f1, 15), relief=GROOVE)
        self.todatelabel.place(x=550, y=10, height=25)

        self.tocal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                             foreground='white', borderwidth=2, state="readonly")
        self.tocal.place(x=750, y=10, height=25)

        self.stafflabel =Label(self.lf2, text="STAFF NAME", bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)
        self.stafflabel.place(x=100, y=100, height=25)

        query = """ select empno, fname, mname, lname from staff"""
        a = self.conn.execute(query).fetchall()
        self.staffinfo = []

        self.listframe = Frame(self.lf2)
        self.listframe.place(x=400, y=100, height=300, width=300)
        self.staffbox = Listbox(self.listframe, font=(self.f1, 15), selectmode="single", selectbackground="yellow")
        for i in a:
            self.staffinfo.append(i)
            self.staffbox.insert(END, i)
        self.staffbox.place(height=300, width=300)
        yscrollbar = Scrollbar(self.listframe)
        yscrollbar.pack(side=RIGHT, fill=Y)
        yscrollbar.config(command=self.staffbox.yview)
        xscrollbar = Scrollbar(self.listframe, orient="horizontal")
        xscrollbar.pack(side=BOTTOM, fill=X)
        xscrollbar.config(command=self.staffbox.xview)

        self.reportbutton = Button(self.lf2, text="Genrate Report For All", bd=5, font=(self.f2, 15), command=self.atreport)
        self.reportbutton.place(x=800, y=450, height=25)

        self.spreportbutton = Button(self.lf2, text="Genrate Report", bd=5, font=(self.f2, 15), command=self.spreport)
        self.spreportbutton.place(x=400, y=450, height=25)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()
