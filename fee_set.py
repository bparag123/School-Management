from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import  Image, ImageTk

class Feeset(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def submit(self):

        try:
            if self.classbox.get() == "CLASS":
                raise ValueError
        except:
            m = messagebox.showerror("School Software","Please select standard")
            return
        try:
            if self.feeentry.get() == "":
                raise ValueError
        except:
            m = messagebox.showerror("School Software","Please enter fee amount")
            return
        try:
            if int(self.feeentry.get()) < 0 :
                raise ValueError
        except:
            m = messagebox.showerror("School Software","Fee amount must be Positive number")
            return

        query = """select standard from fee """
        a = self.conn.execute(query).fetchall()
        temp = []
        for i in a:
            temp.append(str(i[0]))
        if self.classbox.get() in temp:
            query = """update fee set fee = ? where standard = ?"""
            self.conn.execute(query,(self.feeentry.get(), self.classbox.get()))
            self.conn.commit()
        else:
            query = """insert into fee (standard, fee) values (?,?)"""
            self.conn.execute(query,(self.classbox.get(), self.feeentry.get()))
            self.conn.commit()

        m = messagebox.showinfo("School Software","Successful fee change")

        self.c_lassbox.set("CLASS")
        self.fee_entry.set("")
        self.classbox.focus_set()
        self.feeshow()

    def reset(self):
        self.c_lassbox.set("CLASS")
        self.fee_entry.set("")
        self.classbox.focus_set()
        self.feeshow()

    def feeshow(self):
        query = """ select * from fee"""
        a = self.conn.execute(query).fetchall()
        self.txt.config(state="normal")
        self.txt.delete(1.0, END)
        self.txt.insert(END, "\n")
        self.txt.insert(END, "\t\t\t   FEE")
        self.txt.insert(END,"\n\n\t\t Standard \t\t Fee ")
        self.txt.insert(END,"\n\n")
        for i in a:
            self.txt.insert(END,"\n\t\t "+str(i[0])+"\t\t " +str(i[1]))

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

        ##===================================================frame 1====================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))

        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)

        ##=============================================frame 2==========================================================
        self.lf2 = LabelFrame(self, text="SET FEE", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=675)

        self.classlabel = Label(self.lf2, text="STANDARD", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.classlabel.place(x=100, y=100, height=25)

        query = """select standard from master """
        a = self.conn.execute(query).fetchall()
        b = set(a)
        self.cals = []
        temp1 = []
        for i in b:
            temp = str(i[0]).split('-')
            temp1.append(str(temp[0]))
        for i in set(temp1):
            self.cals.append(i)
        self.cals.sort()

        self.c_lassbox = StringVar()
        self.classbox = ttk.Combobox(self.lf2, state="readonly", textvariable=self.c_lassbox, font=(self.f1, 10))
        self.classbox.place(x=300, y=100, height=25, width=200)
        self.classbox['values'] = self.cals
        self.c_lassbox.set("CLASS")

        self.feelabel = Label(self.lf2, text="Fee Amount", bd=2, font=(self.f1,15), fg="white", bg='black',
                              relief=GROOVE)
        self.feelabel.place(x=100, y=200, height=25)

        self.fee_entry = StringVar()
        self.feeentry = Entry(self.lf2, textvariable=self.fee_entry, font=(self.f1, 15))
        self.feeentry.place(x=300, y=200, height=25, width=200)

        self.submitbutton = Button(self.lf2, text="Submit", font=(self.f2, 15), bd=5, command=self.submit)
        self.submitbutton.place(x=100, y=450, height=30)

        self.resetbutton = Button(self.lf2, text="Reset", font=(self.f2, 15), bd=5, command=self.reset)
        self.resetbutton.place(x=350, y=450, height=30)
        self.classbox.focus_set()

        ##======================================================frame 3=================================================
        self.lf3 = LabelFrame(self, text="FEES PREVIEW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf3.place(x=675, y=150, height=550, width=675)

        self.sc = Scrollbar(self.lf3)
        self.txt = Text(self.lf3, yscrollcommand=self.sc.set, borderwidth=2, relief=SUNKEN)
        self.sc.pack(side=RIGHT, fill=Y)
        self.txt.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.sc.config(command=self.txt.yview)
        self.feeshow()

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()

root = Tk()
Feeset(root, root)
root.mainloop()