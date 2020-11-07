from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3
from PIL import Image, ImageTk
import json
from reportlab.pdfgen import canvas
import webbrowser
import datetime

class Remaining_fee(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def gen_report(self,event):
        m = messagebox.askyesnocancel("School Software", "Are you really want to Generate Report For Remaining Fees for Student of Standard : '{}' ?".format(self.cb.get()))
        if m == True:
            if self.cb.get() == "Select Standard":
                messagebox.showerror("School Software", "Please Select Standard First !!")
                self.cb.focus_set()
                return
            else:
                pdf = canvas.Canvas("C:\\Reports\\Fees\\report_{}.pdf".format(datetime.date.today()))
                pdf.setPageSize((600, 900))
                pdf.drawString(200, 880 , "-: Remaining Fee Report :-")
                pdf.line(20, 850 , 580 , 850)
                pdf.line(20, 820 , 580 , 820)
                pdf.drawString(30, 835, "Sr No.")
                pdf.drawString(80, 835, "Roll. No.")
                pdf.drawString(150, 835, "Name")
                pdf.drawString(360, 835, "Total")
                pdf.drawString(440, 835, "Remaining")
                pdf.drawString(530, 835, "Paid")
                pdf.drawString(480, 865, "Date : {}".format(datetime.date.today()))
                query = "select rollno,fname,mname,lname,fee,hisfee from master where standard = '{}' order by rollno".format(self.cb.get())
                detail = self.conn.execute(query).fetchall()  
                top = 800
                sr = 1
                for i in detail:
                    if top < 30:
                        pdf.showPage()
                        top = 800
                        pdf.line(20, 850 , 580 , 850)
                        pdf.line(20, 820 , 580 , 820)
                        pdf.drawString(30, 835, "Sr No.")
                        pdf.drawString(80, 835, "Roll. No.")
                        pdf.drawString(150, 835, "Name")
                        pdf.drawString(360, 835, "Total")
                        pdf.drawString(440, 835, "Remaining")
                        pdf.drawString(530, 835, "Paid")
                    if i[5] != None:
                        fee_paid = json.loads(i[5])
                        sum = 0
                        for x in fee_paid.values():
                            sum += int(x)
                        pdf.drawString(535,top, '{}'.format(sum))
                    else:
                        sum = 0
                        pdf.drawString(540,top, '{}'.format(sum))
                    pdf.drawString(450,top, '{}'.format(float(i[4]-float(sum))))
                    pdf.drawString(360,top, '{}'.format(float(i[4])))
                    pdf.drawString(160,top, '{} {} {}'.format(i[1], i[2], i[3]))
                    pdf.drawString(90,top, '{}'.format(i[0]))
                    pdf.drawString(40,top, '{}'.format(sr))
                    sr += 1
                    top -= 15 
                pdf.save()
                messagebox.showinfo("School Software", "You Report Is Generated Succesfully !!")
                webbrowser.open("C:\\Reports\\Fees\\report_{}.pdf".format(datetime.date.today()))    
        elif m == False:
            pass
        else:
            return
    def __init__(self, root, main_root):

        self.main_root = main_root
        self.root = root
        Toplevel.__init__(self)
        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            messagebox.showerror("School","Database Problem")
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.title("Remaining Fee")
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
        self.lf2 = LabelFrame(self, text="Remaining Fee", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        fee_gen_btn = Button(self.lf2, text="Generate Report", bd=5, font=(self.f2,15), command=self.gen_report)
        fee_gen_btn.place(x = 500, y = 450)
        label = Label(self.lf2, text="Standard")
        label.place(x=100, y=90, height=20)
        self.combo_var = StringVar()
        self.cb = Combobox(self.lf2, state="readonly",textvariable=self.combo_var,
                                font=("Arial Bold", 10))
        self.cb.place(x=355, y=90, height=20, width=200)
        query = "Select distinct standard from master"
        self.stds = self.conn.execute(query).fetchall()
        self.cb['values'] = self.stds
        self.cb.set('Select Standard')
        self.cb.bind("<<ComboboxSelected>>", self.gen_report)
        self.protocol("WM_DELETE_WINDOW", self.c_w)

        self.mainloop()