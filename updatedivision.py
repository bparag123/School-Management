from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk


class Updatedivision(Toplevel):

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

            self.tolabel = Label(self.lf2, text="TO", bd=2, bg="black", fg="white", font=(self.f1, 15), relief=GROOVE)
            self.tolabel.place(x=50, y=225, height=25)
            self.t_oclassbox = StringVar()
            self.toclassbox = ttk.Combobox(self.lf2, state="readonly", textvariable=self.t_oclassbox,
                                           font=(self.f1, 10))
            self.toclassbox.place(x=50, y=300, height=25, width=100)
            query = """ select standard from master where div = 1"""
            databasefecthingvariable = self.conn.execute(query).fetchall()
            setofclass = set(databasefecthingvariable)
            temp_fromclassentrysplit = self.fromclassbox.get().split('-')
            self.toclass = []
            for item in setofclass:
                splittoclass=item[0].split('-')
                if splittoclass[0] == temp_fromclassentrysplit[0]:
                    self.toclass.append(item[0])
            self.toclass.remove(self.fromclassbox.get())
            self.toclass.sort()
            self.toclassbox['values'] = self.toclass
            self.t_oclassbox.set("Select")
            self.rolllabel = Label(self.lf2, text="Student's", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                   relief=GROOVE)
            self.rolllabel.place(x=350, y=85, height=25)
            query1 = """ select rollno, fname, mname, lname  from master where standard = ? """
            a = self.conn.execute(query1, (self.fromclassbox.get(),)).fetchall()
            self.rno = []
            for i in a:
                self.rno.append(i)
            self.rno.sort()
            self.frame = Frame(self.lf2)
            self.frame.place(x=350, y=150, height=300, width=400)
            self.rnobox = Listbox(self.frame, font=(self.f1, 15), selectmode="multiple", selectbackground="yellow")
            for i in self.rno:
                self.rnobox.insert(END, i)
            self.rnobox.place(height=300,width=400)
            yscrollbar = Scrollbar(self.frame)
            yscrollbar.pack(side=RIGHT, fill=Y)
            yscrollbar.config(command=self.rnobox.yview)
            xscrollbar = Scrollbar(self.frame, orient="horizontal")
            xscrollbar.pack(side=BOTTOM, fill=X)
            xscrollbar.config(command=self.rnobox.xview)
            self.rollcounter = 1
        else:
            self.frame.destroy()
            self.rolllabel.destroy()
            self.rnobox.destroy()
            self.tolabel.destroy()
            self.toclassbox.destroy()
            self.rollcounter = 0
            self.rollno()

    def updatediv(self, event=""):

        try:
            if(self.fromclassbox.get() == "CLASS"):
                raise ValueError
        except:
            m = messagebox.showerror("School Software", "please select from  standard", parent=self)
            self.fromclassbox.focus_set()
            return
        try:
            if(self.toclassbox.get() == "Select"):
                raise ValueError
        except:
            m =  messagebox.showerror("School Software", "please select to standard", parent=self)
            self.toclassbox.focus_set()
            return

        query = """ update master set standard = ?, div = ? where rollno = ? and standard = ?"""
        y = self.rnobox.curselection()
        for item in y:
            self.rollnumber = self.rno[item]
            self.conn.execute(query, (self.toclassbox.get(), 1, self.rollnumber[0], self.fromclassbox.get()))
            self.conn.commit()
        self.destroy()
        self.__init__(self, self.main_root)

    def __init__(self, root, main_root):

        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            m = messagebox.showerror("School Software","Couldn't Connect With Database !", parent=self)

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
        self.title("Division")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)

        self.rollcounter = 0

        ##======================================================frame 1=================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), bg="white", command=self.backf)
        bb.place(x=10, y=10)


        ##====================================================frame 2===================================================

        self.lf2 = LabelFrame(self, text="Division", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.classlabel = Label(self.lf2, text="FROM", bd=2, bg="black", fg="white", font=(self.f1, 15),
                                relief=GROOVE)
        self.classlabel.place(x=50, y=85, height=25)

        query = """select standard from master where div = ? """
        a = self.conn.execute(query,(1,)).fetchall()
        b = set(a)
        self.cals = []
        for i in b:
            if (str(i[0])):
                self.cals.append(i[0])
        self.cals.sort()

        self.f_romclassbox = StringVar()
        self.fromclassbox = ttk.Combobox(self.lf2, state="readonly", textvariable=self.f_romclassbox, font=(self.f1, 10))
        self.fromclassbox.place(x=50, y=150, height=25, width=100)
        self.fromclassbox['values'] = self.cals
        self.fromclassbox.bind("<<ComboboxSelected>>", self.rollno)
        self.f_romclassbox.set("CLASS")

        self.updatedivbutton = Button(self.lf2, text="Update ", bd=5, font=(self.f2, 15),
                                      command=self.updatediv)
        self.updatedivbutton.place(x=1000, y=225, height=25)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()