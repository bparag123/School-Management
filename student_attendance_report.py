from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import json
from datetime import date, timedelta
from reportlab.pdfgen import canvas
import webbrowser

class StudentAttendanceReport(Toplevel):

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

    def std_combo_method(self,event=""):

        self.rnolabel = Label(self.lf2, text="ROll Number", bd=2, bg="black", fg="White", font=(self.f1, 15), relief=GROOVE)
        self.rnolabel.place(x=600, y=250, height=25)

        query1 = "select rollno from master where standard = '"+str(self.std_combo.get())+"'"
        roll_list=self.conn.execute(query1).fetchall()
        x = set(roll_list)
        self.rollno = []
        for i in x:
            self.rollno.append(i[0])
        self.rollno.sort()
        self.combo_roll_var = StringVar()
        self.roll_combo = ttk.Combobox(self.lf2,values=self.rollno, textvariable=self.combo_roll_var ,height=20,state="readonly")
        self.roll_combo.place(x=900,y=250, height=25)
        self.combo_roll_var.set("Select")

    def generate_report_method(self, event=""):
        try:
            if self.from_cal.get_date() == self.to_cal.get_date():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "You cannot genrate report because both date same ", parent=self)
            self.from_cal.focus_set()
            return
        try:
            if self.from_cal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You can not genrate feature report", parent=self)
            self.from_cal.focus_set()
            return
        try:
            if self.to_cal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You can not genrate feature report", parent=self)
            self.to_cal.focus_set()
            return
        try:
            if self.std_combo.get() == "Select":
                raise ValueError
        except:
            m = messagebox.showerror("School Software","Please select standard", parent=self)
            return
        try:
            if self.roll_combo.get =="Select":
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "Please select standard", parent=self)
            return

        query1 = "select abday,grno,fname,mname,lname from master where rollno = ? and standard = ?"
        self.data = self.conn.execute(query1,(self.roll_combo.get(),self.std_combo.get())).fetchone()
        self.returned_none = False
        if self.data[0] is not None:
            self.abday_list = json.loads(self.data[0])
        else:
            self.returned_none = True
        self.report_pdf()

    def generate_report_all_method(self, event=""):
        try:
            if self.from_cal.get_date() == self.to_cal.get_date():
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "You cannot genrate report because both date same ", parent=self)
            self.from_cal.focus_set()
            return
        try:
            if self.from_cal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You can not genrate feature report", parent=self)
            self.from_cal.focus_set()
            return
        try:
            if self.to_cal.get_date() > date.today():
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You can not genrate feature report", parent=self)
            self.to_cal.focus_set()
            return
        try:
            if self.std_combo.get() == "Select":
                raise ValueError
        except:
            m = messagebox.showerror("School Software","Please select standard", parent=self)
            return
        query1 = "select rollno, abday,fname,mname,lname from master where standard = ?"
        self.data = self.conn.execute(query1, (self.std_combo.get(),)).fetchall()
        self.abday_all_list = []
        for item in self.data:
            if item[1] != None:
                self.abday_all_list.append(json.loads(item[1]))
            else:
                self.abday_all_list.append("-")

        self.report_all_pdf()

    def report_all_pdf(self):
        pdf = canvas.Canvas("C:\\Reports\\Attendence\\Student\\report_all_{}_{}_to_{}.pdf".format(self.std_combo.get(),
                                                                       self.from_cal.get_date(),self.to_cal.get_date()))
        pdf.setPageSize((600, 900))
        pdf.setFont("Courier-Bold", 20)
        pdf.drawString(200, 880, "Attendence Report")
        pdf.setFont("Courier-Bold", 15)
        pdf.drawString(30, 800, "Roll no ")
        pdf.drawString(300, 800, "Absent Dates")
        pdf.drawString(30, 860, "Standard : {}".format(self.std_combo.get()))
        pdf.drawString(30, 840, "From Date : {}".format(self.from_cal.get_date()))
        pdf.drawString(300, 840, "To Date : {}".format(self.to_cal.get_date()))
        pdf.line(30, 820, 580, 820)
        pdf.line(30, 780, 580, 780)
        top = 740
        line = False
        total_length = len(self.data)
        for i in range(total_length):
            x = len(self.abday_all_list[i])
            for j in range(x):
                if top < 30:
                    pdf.showPage()
                    top = 830
                    pdf.setFont("Courier-Bold", 15)
                    pdf.drawString(30, 865, "Roll no ")
                    pdf.drawString(300, 865, "Absent Dates")
                    pdf.line(30, 880, 580, 880)
                    pdf.line(30, 860, 580, 860)
                if j == 0:
                    emp = "{}-{} {} {}".format(self.data[i][0], self.data[i][2], self.data[i][3],self.data[i][4])
                    pdf.drawString(50, top, emp)
                if self.abday_all_list[i][j] == '-':
                    line = True
                    pdf.drawString(320, top, "-")
                    top -= 15
                else:

                    if str(self.from_cal.get_date()) <= str(self.abday_all_list[i][j]) and str(self.to_cal.get_date()) >= str(
                        self.abday_all_list[i][j]):
                        line = True
                        pdf.drawString(320, top, str(self.abday_all_list[i][j]))
                        top -= 15
            if line:
                pdf.line(50, top, 560, top)
                top -= 15

        pdf.save()
        webbrowser.open("C:\\Reports\\Attendence\\Student\\report_all_{}_{}_to_{}.pdf".format(self.std_combo.get(),self.from_cal.get_date(),
                                                                                         self.to_cal.get_date()))

    def report_pdf(self):

        pdf = canvas.Canvas("C:\\Reports\\Attendence\\Student\\report_{}_{}_{}_to_{}.pdf".format(self.std_combo.get() , self.roll_combo.get(), self.from_cal.get_date(), self.to_cal.get_date()) )
        pdf.setPageSize((600,900))
        pdf.line(10,700,590,700)
        pdf.line(10,860,590,860)
        pdf.line(20,690,20,870)
        pdf.line(580,690,580,870)
        pdf.setFont("Courier-Bold", 20)
        pdf.drawString(200,880,"Attendence Report")
        pdf.setFont("Courier-Bold", 15)
        pdf.drawString(30,840,"Student Name : {} {} {}".format(self.data[2], self.data[3], self.data[4]))
        pdf.drawString(30,815,"Standard : {}".format(self.std_combo.get()))
        pdf.drawString(30,790,"Roll No : {}".format(self.roll_combo.get()))
        pdf.drawString(30,765,"Gr No : {}".format(self.data[1]))
        pdf.drawString(30,740,"From Date : {}".format(self.from_cal.get_date()))
        pdf.drawString(30,715,"To Date : {}".format(self.to_cal.get_date()))
        pdf.line(35, 670, 550 , 670)
        pdf.drawString(40, 655, "Sr No.")
        pdf.drawString(300, 655, "Absent Dates")
        pdf.line(35, 650, 550 , 650)
        pdf.line(120, 670, 120 , 30)
        top = 620
        sr = 1

        if not self.returned_none:
            for i in self.abday_list:
                if top<30:
                    pdf.showPage()
                    top = 830
                    pdf.setFont("Courier-Bold", 15)
                    pdf.drawString(40, 855, "Sr No.")
                    pdf.drawString(300, 855, "Absent Dates")
                    pdf.line(35, 870, 550 , 870)
                    pdf.line(35, 850, 550 , 850)
                    pdf.line(120, 870, 120 , 30)
                pdf.drawString(50, top, str(sr))
                pdf.drawString(320, top, str(i))
                
                top -= 15
                sr += 1
        else:
            pdf.drawString(50, 500, "There is No Absent Days Recorded for This Student !")

        pdf.save()
        webbrowser.open("C:\\Reports\\Attendence\\Student\\report_{}_{}_{}_to_{}.pdf".format(self.std_combo.get() , self.roll_combo.get(), self.from_cal.get_date(), self.to_cal.get_date()))

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
        self.title("ATTENDANCE REPORT")
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
        self.lf2 = LabelFrame(self, text="ATTENDANCE WINDOW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.from_date_label = Label(self.lf2,text='From :', bd=2, bg="black", fg="White", font=(self.f1, 15), relief=GROOVE)
        self.from_date_label.place(x=100,y=100, height=25)

        self.from_cal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                             foreground='white', borderwidth=2, state="readonly")
        self.from_cal.place(x=200,y=100, height=25)

        self.to_date_label = Label(self.lf2, text='To :', bd=2, bg="black", fg="White", font=(self.f1, 15), relief=GROOVE)
        self.to_date_label.place(x=500, y=100, height=25)

        self.to_cal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                             foreground='white', borderwidth=2, state="readonly")
        self.to_cal.place(x=600, y=100, height=25)

        self.stdlabel = Label(self.lf2, text="Standard", bd=2, bg="black", fg="White", font=(self.f1, 15), relief=GROOVE)
        self.stdlabel.place(x=100, y=250, height=25)

        query1 = "select standard from master"
        standard_list = self.conn.execute(query1).fetchall()
        b = set(standard_list)
        self.student = []
        for i in b:
            self.student.append(i[0])
        self.combo_std_var = StringVar()
        self.std_combo = ttk.Combobox(self.lf2,values=self.student, textvariable =self.combo_std_var , height=10,state="readonly")
        self.std_combo.place(x=300,y=250, height=25)
        self.std_combo.bind("<<ComboboxSelected>>",self.std_combo_method)
        self.combo_std_var.set("Select")

        self.report_button = Button(self.lf2, text='Generate Report', bd=5, font=(self.f2, 15),
                                    command=self.generate_report_method)
        self.report_button.place(x=300, y=450)
        self.report_button = Button(self.lf2, text='Generate Report For All Student', bd=5, font=(self.f2, 15),
                                    command=self.generate_report_all_method)
        self.report_button.place(x=700, y=450)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()