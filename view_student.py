from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from datetime import date


class ViewStudent(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def std_combo_method(self,event=""):
        query1 = "select rollno from master where standard = '"+str(self.std_combo.get())+"'"
        roll_list=self.conn.execute(query1).fetchall()
        self.rollno = []
        for i in roll_list:
            self.rollno.append(str(i[0]))
        self.rollno.sort()
        self.combo_roll_var = StringVar()
        self.roll_combo = ttk.Combobox(self.lf2,values=self.rollno, textvariable=self.combo_roll_var ,height=20,state="readonly")
        self.roll_combo.place(x=675,y=10, height=25)
        self.roll_combo.bind("<<ComboboxSelected>>",self.view_method)
        self.combo_roll_var.set("Select")

    def view_method(self,event=""):
        self.grno_label = Label(self.lf2, text="GR no.", bd=2, bg="black", fg="white",relief=GROOVE)
        self.grno_label.place(x=550, y=50, height=25)
        self.std_label=Label(self.lf2,text='Std. :', bd=2, bg="black", fg="white",relief=GROOVE)
        self.std_label.place(x=550,y=90,height=25)
        self.rollno_label = Label(self.lf2,text='Roll no. :', bd=2, bg="black", fg="white",relief=GROOVE)
        self.rollno_label.place(x=550,y=130, height=25)

        self.stdvar = StringVar()
        self.firstnamevar = StringVar()
        self.middlenamevar = StringVar()
        self.lastnamevar = StringVar()
        self.studentphnovar = StringVar()
        self.parentphnovar = StringVar()
        self.emailvar = StringVar()
        self.parent_office_phnovar = StringVar()
        self.feevar = StringVar()
        self.dobvar = StringVar()
        self.categoryvar = StringVar()
        self.bloodgroupvar = StringVar()
        self.castvar = StringVar()

        self.firstname_label = Label(self.lf2, text="First name", bd=2, bg="black", fg="white",relief=GROOVE)
        self.firstname_label.place(x=50, y=50, height=25)
        self.firstnameentry = Entry(self.lf2, textvariable=self.firstnamevar)
        self.firstnameentry.place(x=300, y=50, height=25, width=150)

        self.middlename_label = Label(self.lf2, text="Middle name", bd=2, bg="black", fg="white",relief=GROOVE)
        self.middlename_label.place(x=50, y=90, height=25)
        self.middlenameentry = Entry(self.lf2, textvariable=self.middlenamevar, bd=2, bg="black", fg="white",relief=GROOVE)
        self.middlenameentry.place(x=300, y=90, height=25, width=150)

        self.lastname_label = Label(self.lf2, text="Last name", bd=2, bg="black", fg="white",relief=GROOVE)
        self.lastname_label.place(x=50, y=130, height=25)
        self.lastnameentry = Entry(self.lf2, textvariable=self.lastnamevar)
        self.lastnameentry.place(x=300, y=130, height=25, width=150)

        self.address_label = Label(self.lf2, text="Address", bd=2, bg="black", fg="white",relief=GROOVE)
        self.address_label.place(x=50, y=170, height=25)
        self.addressentry = Text(self.lf2, width=20, height=5, padx=2, pady=2, wrap=WORD)
        self.addressentry.place(x=300, y=170, height=75, width=150)

        self.studentphno_label = Label(self.lf2, text="Student ph.", bd=2, bg="black", fg="white",relief=GROOVE)
        self.studentphno_label.place(x=50, y=260, height=25)
        self.student_phno_entry = Entry(self.lf2, textvariable=self.studentphnovar)
        self.student_phno_entry.place(x=300, y=260, height=25, width=150)

        self.parentphno_label = Label(self.lf2, text="Parent ph.", bd=2, bg="black", fg="white",relief=GROOVE)
        self.parentphno_label.place(x=50, y=300, height=25)
        self.parent_phno_entry = Entry(self.lf2, textvariable=self.parentphnovar)
        self.parent_phno_entry.place(x=300, y=300, height=25, width=150)

        self.email_label = Label(self.lf2, text="Email id", bd=2, bg="black", fg="white",relief=GROOVE)
        self.email_label.place(x=50, y=340, height=25)
        self.emailentry = Entry(self.lf2, textvariable=self.emailvar)
        self.emailentry.place(x=300, y=340, height=25, width=150)

        self.parentadd_label = Label(self.lf2, text="Parent office add.", bd=2, bg="black", fg="white",relief=GROOVE)
        self.parentadd_label.place(x=50, y=380, height=25)
        self.parent_office_add_entry = Text(self.lf2, width=20, height=5, padx=2, pady=2, wrap=WORD)
        self.parent_office_add_entry.place(x=300, y=380, height=75, width=150)

        self.parentoffphno_label = Label(self.lf2, text="Parent office ph.", bd=2, bg="black", fg="white",relief=GROOVE)
        self.parentoffphno_label.place(x=550, y=170, height=25)
        self.parent_office_phno_entry = Entry(self.lf2)
        self.parent_office_phno_entry.place(x=800, y=170, height=25, width=150)

        self.fee_label = Label(self.lf2, text="Fees", bd=2, bg="black", fg="white",relief=GROOVE)
        self.fee_label.place(x=550, y=210, height=25)
        self.feesentry = Entry(self.lf2, textvariable=self.feevar)
        self.feesentry.place(x=800, y=210, height=25, width=150)

        self.dob_label=Label(self.lf2,text="DOB", bd=2, bg="black", fg="white",relief=GROOVE)
        self.dob_label.place(x=550,y=250,height=25)
        self.dob_entry= Entry(self.lf2,textvariable=self.dobvar)
        self.dob_entry.place(x=800,y=250,height=25,width=150)

        self.category_label = Label(self.lf2, text="Category", bd=2, bg="black", fg="white",relief=GROOVE)
        self.category_label.place(x=550, y=290, height=25)
        self.category_entry = Entry(self.lf2,textvariable=self.categoryvar)
        self.category_entry.place(x=800, y=290, height=25, width=150)

        self.bloodgroup_label = Label(self.lf2, text="Blood Group", bd=2, bg="black", fg="white",relief=GROOVE)
        self.bloodgroup_label.place(x=550, y=330, height=25)
        self.bloodgroup_entry = Entry(self.lf2,textvariable=self.bloodgroupvar)
        self.bloodgroup_entry.place(x=800, y=330, height=25, width=150)

        self.cast_label = Label(self.lf2, text="Cast", bd=2, bg="black", fg="white",relief=GROOVE)
        self.cast_label.place(x=550, y=370, height=25)
        self.cast_entry = Entry(self.lf2,textvariable=self.castvar)
        self.cast_entry.place(x=800, y=370, height=25, width=150)

        query2 = "select * from master where standard = ? and rollno = ?"
        self.student_detail = self.conn.execute(query2, (self.std_combo.get(), self.roll_combo.get())).fetchone()

        self.grnotext = Label(self.lf2, text=self.student_detail[0])
        self.grnotext.place(x=800, y=50, height=25)

        self.stdtext = Label(self.lf2, text=self.student_detail[2])
        self.stdtext.place(x=800, y=90, height=25)

        self.rollnotext = Label(self.lf2, text=self.student_detail[1])
        self.rollnotext.place(x=800, y=130, height=25)

        self.firstnamevar.set(self.student_detail[4])
        self.middlenamevar.set(self.student_detail[5])
        self.lastnamevar.set(self.student_detail[6])
        self.addressentry.insert(END,self.student_detail[7])
        self.studentphnovar.set(self.student_detail[8])
        self.parentphnovar.set(self.student_detail[9])
        self.emailvar.set(self.student_detail[10])
        self.parent_office_add_entry.insert(END,self.student_detail[11])
        self.parent_office_phnovar.set(self.student_detail[12])
        self.feevar.set(self.student_detail[13])
        self.dobvar.set(self.student_detail[16])
        self.categoryvar.set(self.student_detail[17])
        self.bloodgroupvar.set(self.student_detail[18])
        self.castvar.set(self.student_detail[19])

        self.firstnameentry.config(state="disabled")
        self.middlenameentry.config(state="disabled")
        self.lastnameentry.config(state="disabled")
        self.addressentry.config(state='disabled')
        self.student_phno_entry.config(state='disabled')
        self.parent_phno_entry.config(state='disabled')
        self.emailentry.config(state='disabled')
        self.parent_office_add_entry.config(state='disabled')
        self.parent_office_phno_entry.config(state='disabled')
        self.feesentry.config(state='disabled')
        self.dob_entry.config(state='disabled')
        self.category_entry.config(state='disabled')
        self.bloodgroup_entry.config(state='disabled')
        self.cast_entry.config(state='disabled')

        self.generate_button = Button(self.lf2,text="Generate Report",command=self.student_report_pdf_method)
        self.generate_button.place(x=500,y=450)

        self.cancel_button = Button(self.lf2, text="Cancel", command=self.cancel_method)
        self.cancel_button.place(x=900, y=450)

    def student_report_pdf_method(self):
        pdf = canvas.Canvas("C:\\Reports\\View\\Student\\report_{}_{}.pdf".format(self.std_combo.get(), self.roll_combo.get()))
        pdf.setPageSize((600, 900))
        pdf.line(10, 700, 590, 700)
        pdf.line(10, 860, 590, 860)
        pdf.line(20, 690, 20, 870)
        pdf.line(580, 690, 580, 870)
        pdf.setFont("Courier-Bold", 20)
        pdf.drawString(220, 880, "SCHOOL NAME")
        pdf.drawString(200, 840, "Student-Info")
        pdf.setFont("Courier-Bold",15)
        pdf.drawString(30, 815, "Student Name : {} {} {}".format(self.student_detail[4], self.student_detail[5], self.student_detail[6]))
        pdf.drawString(30, 790, "Standard : {}".format(self.std_combo.get()))
        pdf.drawString(30, 765, "Roll No : {}".format(self.roll_combo.get()))
        pdf.drawString(30, 740, "Gr No : {}".format(self.student_detail[0]))
        pdf.drawString(30, 715, "Date : {}".format(date.today()))
        pdf.setFont("Courier-Bold",12)
        pdf.drawString(30, 680, "Address : {}".format(self.student_detail[7]))
        pdf.drawString(30, 617.28, "Student phone no. : {}".format(self.student_detail[8]))
        pdf.drawString(30, 554.56, "Parent phone no. : {}".format(self.student_detail[9]))
        pdf.drawString(30, 491.84, "Email : {}".format(self.student_detail[10]))
        pdf.drawString(30, 429.12, "Parent-office address : {}".format(self.student_detail[11]))
        pdf.drawString(30, 366.4, "Parent-office phone number : {}".format(self.student_detail[12]))
        pdf.drawString(30, 303.68, "Fee : {}".format(self.student_detail[13]))
        pdf.drawString(30, 240.96, "DOB : {}".format(self.student_detail[16]))
        pdf.drawString(30, 178.24, "Category : {}".format(self.student_detail[17]))
        pdf.drawString(30, 115.52, "Blood-group : {}".format(self.student_detail[18]))
        pdf.drawString(30, 52.8, "Cast : {}".format(self.student_detail[19]))
        pdf.save()
        self.cancel_method()

    def cancel_method(self):
        self.grno_label.destroy()
        self.std_label.destroy()
        self.rollno_label.destroy()
        self.firstname_label.destroy()
        self.middlename_label.destroy()
        self.lastname_label.destroy()
        self.address_label.destroy()
        self.studentphno_label.destroy()
        self.parentphno_label.destroy()
        self.email_label.destroy()
        self.parentadd_label.destroy()
        self.parentoffphno_label.destroy()
        self.fee_label.destroy()
        self.dob_label.destroy()
        self.category_label.destroy()
        self.bloodgroup_label.destroy()
        self.cast_label.destroy()

        self.grnotext.destroy()
        self.stdtext.destroy()
        self.rollnotext.destroy()
        self.firstnameentry.destroy()
        self.middlenameentry.destroy()
        self.lastnameentry.destroy()
        self.addressentry.destroy()
        self.student_phno_entry.destroy()
        self.parent_phno_entry.destroy()
        self.emailentry.destroy()
        self.parent_office_add_entry.destroy()
        self.parent_office_phno_entry.destroy()
        self.feesentry.destroy()
        self.dob_entry.destroy()
        self.category_entry.destroy()
        self.bloodgroup_entry.destroy()
        self.cast_entry.destroy()

        self.generate_button.destroy()
        self.cancel_button.destroy()
        self.roll_combo.destroy()
        self.combo_std_var.set("Select")


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
        self.title("VIEW STUDENT")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)

        ##==================================================frame 2=====================================================

        self.lf2 = LabelFrame(self, text="VIEW STUDENT", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        query1 = "select distinct standard from master"
        self.standard_list = self.conn.execute(query1).fetchall()
        self.combo_std_var = StringVar()
        self.std_combo = ttk.Combobox(self.lf2, values=self.standard_list, textvariable=self.combo_std_var, height=10,
                                      state="readonly")
        self.std_combo.place(x=100, y=10, height=25)
        self.std_combo.bind("<<ComboboxSelected>>", self.std_combo_method)
        self.combo_std_var.set("Select")

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()