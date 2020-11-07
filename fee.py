from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import  Image, ImageTk
from datetime import date
import json
from reportlab.pdfgen import canvas
import webbrowser

class fee1(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def rollno(self, event=""):

        if self.rollcounter == 0:
            self.rolllabel = Label(self.lf2, text="ROLL NO", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                   relief=GROOVE)
            self.rolllabel.place(x=300, y=85, height=25)
            query1 = """ select rollno, fname, mname, lname from master where standard = ?"""
            a = self.conn.execute(query1, (self.classbox.get(), )).fetchall()
            self.rno = []
            for i in a:
                self.rno.append(i)
            self.rno.sort()
            self.r_ollbox = StringVar()
            self.rollbox = ttk.Combobox(self.lf2, state="readonly", textvariable=self.r_ollbox, font=(self.f1, 10))
            self.rollbox.place(x=300, y=150, height=25, width=300)
            self.rollbox['values'] = self.rno
            self.rollbox.set("Select")
            self.rollbox.bind("<<ComboboxSelected>>", self.amountoffee)
            self.rollcounter = 1
        else:
            self.rolllabel.destroy()
            self.rollbox.destroy()
            self.rollcounter = 0
            self.rollno()

    def amountoffee(self, event=""):

        if self.feecounter == 0:
            b = self.rollbox.get()
            self.r = b.split(' ')
            self.tfeelabel = Label(self.lf2, text="Total Fee", bd=2, bg="black", fg="white",font=(self.f1, 12),
                                  relief=GROOVE)
            self.tfeelabel.place(x=70, y=275, height=25)

            query = """ select fee from master where standard=? AND rollno=?"""
            a = self.conn.execute(query,(self.classbox.get(), self.r[0])).fetchone()
            self.feeamount = a[0]
            self.t_feeentry = StringVar()
            self.tfeeentry = Entry(self.lf2, textvariable=self.t_feeentry, font=(self.f1,10))
            self.tfeeentry.place(x=50, y=350, height=25, width=150)
            self.tfeeentry.config(state="disabled")
            self.t_feeentry.set(self.feeamount)

            self.pfeelabel = Label(self.lf2, text="Payment", bd=2, bg="black", fg="white", font=(self.f1, 12),
                                   relief=GROOVE)
            self.pfeelabel.place(x=470, y=275, height=25)
            self.p_feeentry = StringVar()
            self.pfeeentry = Entry(self.lf2, textvariable=self.p_feeentry, font=(self.f1,10))
            self.pfeeentry.place(x=450, y=350, height=25, width=150)
            self.rfeelabel = Label(self.lf2,text="Fee to be Paid", bd=2, bg="black", fg="white", font=(self.f1,12), relief=GROOVE)
            self.rfeelabel.place(x=250, y=275, height=25)
            self.r_feeentry = StringVar()
            self.rfeeentry = Entry(self.lf2, textvariable=self.r_feeentry, font=(self.f1,10))
            self.rfeeentry.place(x=250, y=350, height=25, width=150)
            self.rfeeentry.config(state="disabled")
            query = """ select hisfee from master where standard=? and rollno=? """
            a = self.conn.execute(query, (self.classbox.get(), self.r[0])).fetchone()
            if a[0] == None:
                query = """ select fee from master where standard=? and rollno=? """
                b = self.conn.execute(query, (self.classbox.get(), self.r[0])).fetchone()
                self.r_feeentry.set(b[0])
            else:
                x = json.loads(a[0])
                sum = int()
                for i in x.values():
                    sum +=int(i)
                query = """ select fee from master where standard=? and rollno=? """
                b = self.conn.execute(query, (self.classbox.get(), self.r[0])).fetchone()
                self.r_feeentry.set(b[0]-sum)
            self.feecounter = 1
        else:
            self.pfeeentry.destroy()
            self.pfeelabel.destroy()
            self.tfeeentry.destroy()
            self.tfeelabel.destroy()
            self.rfeeentry.destroy()
            self.rfeelabel.destroy()
            self.feecounter = 0
            self.amountoffee()

    def fee_pdf(self,pdf):
        pdf.line(10, 20, 590, 20)
        pdf.line(10, 430, 590, 430)
        pdf.line(20, 10, 20, 440)
        pdf.line(580, 10, 580, 440)
        pdf.line(30, 380, 570, 380)
        pdf.setFont("Courier-Bold", 20)
        pdf.drawString(220, 410, "School Name")
        pdf.setFont("Courier-Bold", 10)
        pdf.drawString(230, 370, "-: FEE RECEIPT :-")
        pdf.drawString(220, 390, "Email : ")
        pdf.drawString(420, 390, "Phone No. : ")
        pdf.setFont("Courier-Bold", 10)
        pdf.drawString(30, 350, "Date :")
        pdf.line(70, 350, 150, 350)
        pdf.drawString(170, 350, "Receipt No :")
        pdf.line(245, 350, 280, 350)
        pdf.drawString(300, 350, "Receiver ID :")
        pdf.line(380, 350, 410, 350)
        pdf.drawString(430, 350, "Payment Mode :")
        pdf.line(515, 350, 560, 350)
        pdf.setFont("Courier-Bold", 13)

        pdf.drawString(30, 330, "Student Name :")
        pdf.drawString(30, 315, "Standard     :")
        pdf.drawString(30, 300, "Roll No      :")

        pdf.setFont("Courier-Bold", 10)

        pdf.drawString(50,264,"Sr.")
        pdf.drawString(125, 264, "Description")
        pdf.drawString(328, 270, "Fee Paid")
        pdf.drawString(330, 260, "(Today)")
        pdf.drawString(430, 270, "Fee Remaining")
        pdf.drawString(455, 260, "(Now)")
        pdf.line(300,280,300,150)
        pdf.line(400,280,400,150)

        pdf.line(80, 280, 80, 150)

        pdf.line(30, 280, 560, 280)
        pdf.line(30, 250, 560, 250)

        pdf.line(30, 150, 560, 150)

        pdf.setFont("Courier-Bold", 13)
        pdf.drawString(30, 120, "Cheque No. :")
        pdf.drawString(30, 105, "Total Fee : {}".format(self.feeamount))
        pdf.drawString(30, 90, "Last Remaining : {}".format(self.r_feeentry.get()))
        pdf.drawString(480, 50, "Signature")
        pdf.drawString(478, 35, "(Receiver)")
        pdf.line(470, 65, 565, 65)


        #===================================

        pdf.setFont("Courier-Bold", 10)
        pdf.drawString(80,352,str(date.today()))
        pdf.drawString(255,352,'1')
        pdf.drawString(390,352,'1')
        pdf.drawString(525,352,'CASH')
        pdf.setFont("Courier-Bold", 13)
        pdf.drawString(170,330,str(self.data[3]))
        pdf.drawString(170,315,str(self.data[2]))
        pdf.drawString(170,300,str(self.data[1]))

        pdf.drawString(120,235,"School Fee")
        pdf.drawString(50,235,'1')
        pdf.drawString(340,235,str(self.p_feeentry.get()))
        remaining = int(self.r_feeentry.get()) - int(self.p_feeentry.get())
        pdf.drawString(440, 235, str(remaining))
        #===================================


        pdf.save()
        webbrowser.open("C:\\Fees\\fee_1_{}_{}.pdf".format(self.classbox.get(),self.data[3]))

    def pay(self,event=""):
        try:
            if self.classbox.get == "CLASS":
                raise ValueError
        except:
            m = messagebox.showerror("School Software","Please select standard", parent=self)
            self.classbox.focus_set()
            return

        try:
            if self.rollbox.get() == "Select":
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "Please select roll no", parent=self)
            self.rollbox.focus_set()
            return
        try:
            if self.pfeeentry.get() == "":
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "Please enter fee amount", parent=self)
            self.pfeeentry.focus_set()
            return
        try:
            if(int(self.pfeeentry.get()) > int(self.rfeeentry.get())):
                raise ValueError
        except:
            m = messagebox.showerror("School Software","You have remaining only '{}' Rs. to pay.".format(self.rfeeentry.get()), parent=self)
            self.pfeeentry.focus_set()
            return

        query = """ select hisfee from master where standard=? and rollno=? """
        a = self.conn.execute(query,(self.classbox.get(), self.r[0])).fetchone()
        self.dic = {}
        newfee = self.feeamount - int(self.pfeeentry.get())

        if a[0] == None:
            self.dic[str(date.today())] = self.pfeeentry.get()
            p = json.dumps(self.dic)
            query = """update master set hisfee=? where standard=? and rollno=?"""
            self.conn.execute(query,(p, self.classbox.get(), self.r[0]))
            self.conn.commit()
        else:
            x = json.loads(a[0])
            x[str(date.today())] = self.pfeeentry.get()
            p = json.dumps(x)
            query = """update master set hisfee=? where standard=? and rollno=?"""
            self.conn.execute(query,(p, self.classbox.get(), self.r[0]))
            self.conn.commit()
        query = """select * from master where standard="{}" and rollno="{}" """.format(self.classbox.get(), self.r[0])
        self.data = self.conn.execute(query).fetchone()
        pdf = canvas.Canvas("C:\\Fees\\fee_1_{}_{}.pdf".format(self.classbox.get(),self.data[3]))
        pdf.setPageSize((600, 450))
        self.fee_pdf(pdf)

        self.pfeeentry.destroy()
        self.pfeelabel.destroy()
        self.tfeeentry.destroy()
        self.tfeelabel.destroy()
        self.rfeeentry.destroy()
        self.rfeelabel.destroy()
        self.rolllabel.destroy()
        self.rollbox.destroy()
        self.rollcounter = 0
        self.feecounter = 0
        self.classbox.set('CLASS')

    def reset(self, event=""):
        self.pfeeentry.destroy()
        self.pfeelabel.destroy()
        self.tfeeentry.destroy()
        self.tfeelabel.destroy()
        self.rfeeentry.destroy()
        self.rfeelabel.destroy()
        self.rolllabel.destroy()
        self.rollbox.destroy()
        self.rollcounter = 0
        self.feecounter = 0
        self.classbox.set('CLASS')

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
        self.title("FEES")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)

        self.rollcounter = 0
        self.feecounter = 0

        ##===================================================frame 1====================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))

        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)

        ##=============================================frame 2==========================================================
        self.lf2 = LabelFrame(self, text="PAY FEE", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=675)

        self.classlabel = Label(self.lf2, text="STANDARD", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.classlabel.place(x=50, y=85, height=25)

        query = """select standard from master """
        a = self.conn.execute(query).fetchall()
        b = set(a)
        self.cals = []
        for i in b:
            self.cals.append(str(i[0]))
        self.cals.sort()

        self.c_lassbox = StringVar()
        self.classbox = ttk.Combobox(self.lf2, state="readonly", textvariable=self.c_lassbox, font=(self.f1, 10))
        self.classbox.place(x=50, y=150, height=25, width=100)
        self.classbox['values'] = self.cals
        self.classbox.bind("<<ComboboxSelected>>", self.rollno)
        self.c_lassbox.set("CLASS")

        self.paybutton = Button(self.lf2, text="PAY", font=(self.f2, 15), bd=5, command=self.pay)
        self.paybutton.place(x=100, y=450, height=25)

        self.resetbutton = Button(self.lf2, text="RESET", font=(self.f2, 15), bd=5, command=self.reset)
        self.resetbutton.place(x=300, y=450, height=25)


        ##======================================================frame 3=================================================
        self.lf3 = LabelFrame(self, text="FEES PREVIEW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf3.place(x=675, y=150, height=550, width=675)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()