from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from datetime import date, timedelta


class RemoveUser(Toplevel):

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

    def lc_pdf(self):
        query = "select * from staff where empno={}".format(self.remove_user_combo.get())
        user_data = self.conn.execute(query).fetchone()
        subject_list = user_data[8].split("-")
        pdf = canvas.Canvas("C:\\Reports\\LC\\report_{}.pdf".format(self.remove_user_combo.get()))
        pdf.setPageSize((900,600))
        pdf.rect(10,10,880,580)
        pdf.setFont("Courier-Bold", 20)
        logo = 'logo.jpg'
        pdf.drawInlineImage(logo, 400, 430)

        pdf.drawString(100, 350, "This is to Cerify that  ")
        pdf.line(380,350,800,350)
        pdf.drawString(385,350,"Mr./Mrs./Miss  {} {} {}".format(user_data[1], user_data[2], user_data[3]))
        pdf.drawString(50, 330, "has worked with")
        pdf.line(250,330,800,330)
        pdf.line(411,310,741,310)
        pdf.drawString(50, 310, "in the capacity of Lecturer of  {}".format(subject_list[1]))
        pdf.drawString(745, 310, "from")
        pdf.line(50,290,300,290)
        pdf.drawString(117, 290, "{}".format(user_data[12]))
        pdf.drawString(310, 290, "as a full time employee.")
        pdf.drawString(100, 250, "He is Valuable Member of management of (School). He always ")
        pdf.drawString(50, 230, "Performed his duties with full zeal & commitment. His Extra ")
        pdf.drawString(50, 210, "efforts were always appreciated by his directors. He has all")
        pdf.drawString(50, 190, "the capabilities of working under stress & critical situations.")
        pdf.drawString(100, 150, "We wish him best of luck & we strongly recommended him")
        pdf.drawString(50, 130, "for any suitable post.")
        pdf.line(700,65,870,65)
        pdf.drawString(730, 45, "Signature")
        pdf.drawString(720, 30, "(Principal)")
        pdf.line(20,65,176,65)
        pdf.drawString(40, 65, "{}".format(date.today()))
        pdf.drawString(75, 45, "Date")
        pdf.save()

    def remove_button_method(self):
        answer = messagebox.askyesno("School Software","Are you sure to want to remove this user")

        if answer>0:
            self.lc_pdf()
            query="delete from staff where empno=" + str(self.remove_user_combo.get())
            self.conn.execute(query)
            self.conn.commit()
            self.remove_user_combo.set("SELECT EMPNO")
            self.firstname.destroy()
            self.middlename.destroy()
            self.lastname.destroy()
            self.salary.destroy()
            self.phoneno.destroy()
            self.firstnameentry.destroy()
            self.middlenameentry.destroy()
            self.lastnameentry.destroy()
            self.salaryentry.destroy()
            self.phonenoentry.destroy()
            self.remove_user_button.destroy()
            query2 = "select empno from staff where currentuser=0;"
            list2 = self.conn.execute(query2).fetchall()
            my_list = []
            for i in list2:
                my_list.append(i)
            self.remove_user_combo.config(values=my_list)
        else:
            return

    def remove_combo_method(self,event=""):
        self.firstname = Label(self.lf2, text='firstname')
        self.middlename = Label(self.lf2, text='middlename')
        self.lastname = Label(self.lf2, text='lastname')
        self.salary = Label(self.lf2, text='salary')
        self.phoneno = Label(self.lf2, text='phoneno')

        self.firstnamevar = StringVar()
        self.firstnameentry = Entry(self.lf2, textvariable=self.firstnamevar)
        self.middlenamevar = StringVar()
        self.middlenameentry = Entry(self.lf2, textvariable=self.middlenamevar)
        self.lastnamevar = StringVar()
        self.lastnameentry = Entry(self.lf2, textvariable=self.lastnamevar)
        self.salaryvar = StringVar()
        self.salaryentry = Entry(self.lf2, textvariable=self.salaryvar)
        self.phonenovar = StringVar()
        self.phonenoentry = Entry(self.lf2, textvariable=self.phonenovar)

        self.firstname.place(x=175, y=202)
        self.firstnameentry.place(x=970, y=202)
        self.middlename.place(x=175, y=252)
        self.middlenameentry.place(x=970, y=252)
        self.lastname.place(x=175, y=302)
        self.lastnameentry.place(x=970, y=302)
        self.salary.place(x=175, y=352)
        self.salaryentry.place(x=970, y=352)
        self.phoneno.place(x=175, y=402)
        self.phonenoentry.place(x=970, y=402)

        query = "select * from staff where empno= " + str(self.remove_user_combo.get())
        staffinfo = self.conn.execute(query).fetchone()

        self.firstnamevar.set(staffinfo[1])
        self.middlenamevar.set(staffinfo[2])
        self.lastnamevar.set(staffinfo[3])
        self.salaryvar.set(staffinfo[4])
        self.phonenovar.set(staffinfo[5])

        self.firstnameentry.config(state="disabled")
        self.middlenameentry.config(state="disabled")
        self.lastnameentry.config(state="disabled")
        self.salaryentry.config(state="disabled")
        self.phonenoentry.config(state="disabled")

        self.remove_user_button = Button(self.lf2,text="remove",command=self.remove_button_method)
        self.remove_user_button.place(x=550,y=450)

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
        self.title("REMOVE STAFF")
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
        self.lf2 = LabelFrame(self, text="Remove User", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        query1 = "select empno from staff where currentuser=0;"
        list1 = self.conn.execute(query1).fetchall()
        my_list = []
        for i in list1:
            my_list.append(i)
        self.remove_user_combo = ttk.Combobox(self.lf2, values=my_list, height=10,state="read only")
        self.remove_user_combo.bind("<<ComboboxSelected>>", self.remove_combo_method)
        self.remove_user_combo.set("SELECT EMPNO")
        self.remove_user_combo.pack()

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()
