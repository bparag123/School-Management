from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
import json


class Delete_Exam(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def get_exam_details(self,event):
        self.combo_get_exam.config(state="disabled")
        self.selected_entry_var = StringVar()
        self.selected_label = Label(self, text="You have selected : ")
        self.selected_label.place(x=200,y=300)
        self.selected_entry = Entry(self, state="disabled", textvariable=self.selected_entry_var)
        self.selected_entry.place(x=400,y=300)
        self.selected_entry_var.set(self.combo_get_exam_var.get())

    def del_exam(self):
        m = messagebox.askyesnocancel("School Software", "Are you really want to Cancle the Exam?")
        if m == True:

            query = """select * from exams"""
            j_fetch = self.conn.execute(query).fetchone()

            self.fetched_data = json.loads(j_fetch[0])
            self.fetched_mark = json.loads(j_fetch[1])


            query = "drop table '{}';".format(self.fetched_data[self.selected_entry_var.get()][-1])
            self.conn.execute(query)
            del self.fetched_data[self.selected_entry_var.get()]
            del self.fetched_mark[self.selected_entry_var.get()]
            j = json.dumps(self.fetched_data)
            j_mark = json.dumps(self.fetched_mark)
            query = """update exams set data=(?), marks=(?)"""
            self.conn.execute(query, (j, j_mark))
            self.conn.commit()
            messagebox.showinfo("School Software", "Your Deletion of Exam : '{}' is Succesful!".format(self.selected_entry_var.get()))
            self.reset()
        elif m == False:
            self.reset()
        else:
            return
    def reset(self):
        self.combo_get_exam.config(state="normal")
        self.combo_get_exam.config(state="readonly")
        self.selected_entry.destroy()
        self.selected_label.destroy()

        #refreshing combodata
        query = "select data from exams"
        j_data = self.conn.execute(query).fetchone()
        data = json.loads(j_data[0])
        exams = data.keys()
        print(type(exams))
        k = []
        for i in exams:
            k.append(i)
        self.combo_get_exam['values'] = k
        self.combo_get_exam.set("Select")

    def __init__(self, root, main_root):

        self.main_root = main_root
        self.root = root
        Toplevel.__init__(self)
        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            messagebox.showerror("School Software","Database Problem")
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.title("Delete Exam")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)
        ##======================================================frame1==================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 20), command=self.backf)
        bb.place(x=10, y=10)
        ##======================================================frame 2=================================================
        self.lf2 = LabelFrame(self, text="DELETE EXAM WINDOW", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)
        self.combo_get_exam_var = StringVar()
        self.combo_get_exam = Combobox(self.lf2, state="readonly", textvariable=self.combo_get_exam_var, font=("Arial Bold", 15))
        self.combo_get_exam.place(x=300, y=100)
        query = "select data from exams"
        j_data = self.conn.execute(query).fetchone()
        data = json.loads(j_data[0])
        exams = data.keys()
        k = []
        for i in exams:
            k.append(i)
        self.combo_get_exam['values'] = k
        self.combo_get_exam.set("Select")
        self.combo_get_exam.bind("<<ComboboxSelected>>", self.get_exam_details)
        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.reset_btn = Button(self.lf2, text="RESET", command=self.reset)
        self.reset_btn.place(x=200,y=450)
        self.reset_btn = Button(self.lf2, text="DELETE", command=self.del_exam)
        self.reset_btn.place(x=500, y=450)
        self.mainloop()
