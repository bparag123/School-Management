from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from mark_entry import Mark_Entry
from delete_exam import Delete_Exam
from update_mark import Update_Mark
from percentage import Percentage
import sqlite3
import json
import time
from tkcalendar import DateEntry

class r1(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def done_sub(self):

        # ======
        if self.subject_entry.get() != "" or self.mark_entry.get() != "" or self.internal_mark_entry.get() != "0":
            if self.exam_entry.get() == "":
                messagebox.showerror("School Software", "Exam Name Should not be Empty.")
                self.exam_entry.focus_set()
                return

            if self.subject_entry.get().isalpha():
                pass
            else:
                messagebox.showerror("School Software", "Subject Name Should not be Empty nor Numeric.")
                self.subject_entry.focus_set()
                return

            try:
                int(self.mark_entry.get())
            except:
                messagebox.showerror("School Software", "Marks Should not be Empty.\nMarks Shold be Positive Number")
                self.mark_entry.focus_set()
                return
            if int(self.mark_entry.get()) < 1:
                messagebox.showerror("School Software", "Marks Should not be Empty.\nMarks Shold be Positive Number")
                self.mark_entry.focus_set()
                return

            try:
                int(self.internal_mark_entry.get())
            except:
                messagebox.showerror("School Software",
                                     "Internal Marks Should not be Empty.\nInternal Marks Shold be Positive Number.")
                self.internal_mark_entry.focus_set()
                return

            if int(self.internal_mark_entry.get()) < 0:
                messagebox.showerror("School Software",
                                     "Internal Marks Should not be Empty.\nInternal Marks Shold be Positive Number.")
                self.internal_mark_entry.focus_set()
                return

            mark = self.mark_entry.get()
            sub = self.subject_entry.get()
            internal = self.internal_mark_entry.get()
            self.subject_list.append(sub)
            internal_subj_column = "{}_internal".format(self.subject_list[-1])
            self.subject_list.append(internal_subj_column)
            self.mark_list.append(mark)
            self.mark_list.append(internal)
        # ========================

        m = messagebox.askyesnocancel("School Software", "Are you really want to Save the Changes?")
        if m == True:

            if self.cb3.get() != "Select":
                pass
            else:
                messagebox.showerror("School Software", "Please Select Standard first.")
                self.cb3.focus_set()
                return

            for i in range(len(self.subject_list)):
                if i == 0:
                    try:
                        query = "CREATE TABLE '{}_{}_{}' (std TEXT, rollno NUMERIC,{} NUMERIC );".format(
                            self.exam_entry.get(), self.combo_var_std_start.get(), str(self.cal.get_date()), self.subject_list[i])
                        self.conn.execute(query)
                    except:
                        messagebox.showerror("School Software",
                                             "You have already Generated Exam : '{}' for Standard : '{}'.\nPlease Complete it or Delete it.".format(
                                                 self.exam_entry.get(), self.combo_var_std_start.get()))
                        self.sub_entry_var.set('')
                        self.mark_entry_var.set('')
                        self.internal_mark_entry_var.set('0')
                        return
                else:
                    try:

                        query = "ALTER TABLE '{}_{}_{}' ADD {} NUMERIC;".format(self.exam_entry.get(),
                                                                                self.combo_var_std_start.get(),
                                                                                str(self.cal.get_date()), self.subject_list[i])
                        self.conn.execute(query)
                    except:
                        messagebox.showerror("School Software",
                                             "You have already Entered Subject : '{}' for Exam : '{}'\nPlease Change The Subject.".format(
                                                 self.subject_list[i], self.exam_entry.get()))
                        self.conn.rollback()
                        query = "drop table '{}_{}_{}'".format(self.exam_entry.get(), self.combo_var_std_start.get(),
                                                               str(self.cal.get_date()))
                        self.conn.execute(query)

                        self.subject_list.remove(self.subject_list[i])
                        self.mark_list.remove(self.mark_list[i])

                        self.subject_list.remove(self.subject_list[i])
                        self.mark_list.remove(self.mark_list[i])
                        self.sub_entry_var.set('')
                        self.subject_entry.focus_set()

                        return
            self.conn.commit()

            query = "select count(*) from exams"
            rows = self.conn.execute(query).fetchone()
            set_exam_name = "{}_{}_{}".format(self.exam_entry.get(), self.combo_var_std_start.get(), str(self.cal.get_date()))
            if rows[0] == 0:
                mark_data = {}
                data = {}
                self.subject_list.append(
                    '{}_{}_{}'.format(self.exam_entry.get(), self.combo_var_std_start.get(), str(self.cal.get_date())))
                data[set_exam_name] = self.subject_list
                mark_data[set_exam_name] = self.mark_list
                j_mark = json.dumps(mark_data)
                j = json.dumps(data)
                query = """insert into exams(data, marks) values(?,?)"""
                self.conn.execute(query, (j, j_mark))
                self.conn.commit()
                messagebox.showinfo("School Software",
                                    "Youe Exam is Genereted Succesfully.\nYour Exam is Generated with Name : '{}'".format(
                                        set_exam_name))
                self.reset()

            else:

                query = """select * from exams"""
                j_fetch = self.conn.execute(query).fetchone()

                fetched_data = json.loads(j_fetch[0])
                fetched_mark = json.loads(j_fetch[1])
                self.subject_list.append(
                    '{}_{}_{}'.format(self.exam_entry.get(), self.combo_var_std_start.get(), str(self.cal.get_date())))
                fetched_data[set_exam_name] = self.subject_list
                fetched_mark[set_exam_name] = self.mark_list
                j = json.dumps(fetched_data)
                j_mark = json.dumps(fetched_mark)
                query = """update exams set data=(?), marks=(?)"""
                self.conn.execute(query, (j, j_mark))
                self.conn.commit()
                messagebox.showinfo("School Software",
                                    "Youe Exam is Genereted Succesfully.\nYour Exam is Generated with Name : '{}'".format(
                                        set_exam_name))
                self.reset()

        elif m == False:

            self.reset()

        else:
            return

    def reset(self):
        self.combo_var_std_start.set("Select")
        self.exam_entry_var.set('')
        self.subject_list = []
        self.mark_list = []
        self.internal_mark_list = []
        self.subject_entry.focus_set()
        self.sub_entry_var.set('')
        self.mark_entry_var.set('')
        self.internal_mark_entry_var.set('0')
        self.exam_entry.focus_set()
        self.done_btn.config(state="disabled")


    def add_sub_and_mark(self):
        if self.exam_entry.get() == "":
            messagebox.showerror("School Software", "Exam Name Should not be Empty.")
            self.exam_entry.focus_set()
            return

        if self.subject_entry.get() == "":
            messagebox.showerror("School Software",  "Subject Name Should not be Empty nor Numeric.")
            self.subject_entry.focus_set()
            return

        if self.subject_entry.get().isalpha():
            pass
        else:
            messagebox.showerror("School Software", "Subject Name Should not be Empty nor Numeric.")
            self.subject_entry.focus_set()
            return

        try:
            int(self.mark_entry.get())
        except:
            messagebox.showerror("School Software", "Marks Should not be Empty.\nMarks Shold be Positive Number")
            self.mark_entry.focus_set()
            return
        if self.mark_entry.get() == "" or int(self.mark_entry.get()) < 1:
            messagebox.showerror("School Software", "Marks Should not be Empty.\nMarks Shold be Positive Number")
            self.mark_entry.focus_set()
            return

        try:
            int(self.internal_mark_entry.get())
        except:
            messagebox.showerror("School Software", "Internal Marks Should not be Empty.\nInternal Marks Shold be Positive Number.")
            self.internal_mark_entry.focus_set()
            return

        if self.internal_mark_entry.get() == "" or int(self.internal_mark_entry.get()) < 0:
            messagebox.showerror("School Software", "Internal Marks Should not be Empty.\nInternal Marks Shold be Positive Number.")
            self.internal_mark_entry.focus_set()
            return

        mark = self.mark_entry.get()
        sub = self.subject_entry.get()
        internal = self.internal_mark_entry.get()
        self.subject_list.append(sub)
        internal_subj_column = "{}_internal".format(self.subject_list[-1])
        self.subject_list.append(internal_subj_column)
        self.mark_list.append(mark)
        self.mark_list.append(internal)
        self.sub_entry_var.set('')
        self.mark_entry_var.set('')
        self.internal_mark_entry_var.set('0')
        self.subject_entry.focus_set()
        self.done_btn.config(state="normal")

    def marks_entry(self):
        self.withdraw()
        Mark_Entry(self, self.main_root)

    def calculate_percentage(self):
        self.withdraw()
        Percentage(self,self.main_root)

    def delete_exam(self):
        self.withdraw()
        Delete_Exam(self,self.main_root)

    def update_marks(self):
        self.withdraw()
        Update_Mark(self,self.main_root)

    def __init__(self,root,main_root):

        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            messagebox.showerror("School","Database Problem")
        self.date = time.strftime("%d_%m_%y")
        self.subject_list = []
        self.mark_list = []
        self.internal_mark_list = []

        self.root = root
        self.main_root = main_root
        Toplevel.__init__(self)
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()

        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.title("EXAMS")
        self.config(background=self.bgclr1)
        self.geometry("1350x700+0+0")
        self.resizable(False, False)

        ##======================================================frame 1================================================
        imagel = Image.open("left-arrow.png")
        imagel = imagel.resize((60, 15))
        imgl = ImageTk.PhotoImage(imagel)

        self.lf1 = LabelFrame(self, text="NAME", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf1.place(x=0, y=0, height=150, width=1350)

        bb = Button(self.lf1, image=imgl, bd=5, font=(self.f1, 10), command=self.backf)
        bb.place(x=10, y=10)
        ##=====================================================frame 2================================================
        self.lf2 = LabelFrame(self, text="CREATE EXAM", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=675)

        label = Label(self.lf2, text="Exam Name")
        label.place(x=100, y=20, height=20)
        label = Label(self.lf2, text="Subjects for Exam")
        label.place(x=100, y=230, height=20)
        label = Label(self.lf2, text="Marks for Subject")
        label.place(x=100, y=300, height=20)
        label = Label(self.lf2, text="Internal Marks for Subject")
        label.place(x=100, y=370, height=20)
        label = Label(self.lf2, text="Standard")
        label.place(x=100, y=90, height=20)
        label = Label(self.lf2, text="Date of Exam")
        label.place(x=100, y=160)
        self.sub_entry_var = StringVar()
        self.mark_entry_var = StringVar()
        self.exam_entry_var = StringVar()
        self.internal_mark_entry_var = StringVar()
        self.internal_mark_entry_var.set('0')
        self.exam_entry = Entry(self.lf2, textvariable=self.exam_entry_var)
        self.exam_entry.place(x=350, y=20, height=20)
        self.combo_var_std_start = StringVar()
        self.cb3 = ttk.Combobox(self.lf2, state="readonly",textvariable=self.combo_var_std_start,
                                font=("Arial Bold", 10))
        self.cb3.place(x=355, y=90, height=20, width=100)
        self.cal = DateEntry(self.lf2, width=12, background='darkblue', date_pattern='dd/mm/yyyy',
                             foreground='white', borderwidth=2, state="readonly")
        self.cal.place(x=350, y=160)
        self.subject_entry = Entry(self.lf2, textvariable=self.sub_entry_var)
        self.subject_entry.place(x=350, y=230, height=20)
        self.mark_entry = Entry(self.lf2, textvariable=self.mark_entry_var)
        self.mark_entry.place(x=350, y=300, height=20)
        self.internal_mark_entry = Entry(self.lf2, textvariable=self.internal_mark_entry_var)
        self.internal_mark_entry.place(x=350, y=370, height=20)

        query = "Select distinct standard from master"
        self.stds = self.conn.execute(query).fetchall()
        self.cb3['values'] = self.stds
        # self.cb3['values'] = ["L.K.G", "H.K.G", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "11~Commerce", "12~Commerce",
        #                       "11~Science", "12~Science"]
        self.cb3.set("Select")
        add_btn = Button(self.lf2, text="ADD Another Subject", font=(self.f1, 10),
                         command=self.add_sub_and_mark)
        add_btn.place(x=80, y=425, width=200)
        self.done_btn = Button(self.lf2, width=30, text="DONE", font=(self.f1, 10),
                               command=self.done_sub)
        self.done_btn.place(x=350, y=425, width=200)
        self.done_btn.config(state="disabled")

        ##===================================================== frame 3===============================================
        self.lf3 = LabelFrame(self, text="Marks Entry & Results", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf3.place(x=675, y=150, height=550, width=675)

        mark_btn = Button(self.lf3, text="MARK ENTRY", command=self.marks_entry)
        mark_btn.place(x=300, y=50, height=25)
        btn = Button(self.lf3, text="Update Marks", command=self.update_marks)
        btn.place(x=300, y=125, height=25)
        btn = Button(self.lf3, text="Delete Exam", command=self.delete_exam)
        btn.place(x=300, y=200, height=25)
        btn = Button(self.lf3, text="Generate Result", command=self.calculate_percentage)
        btn.place(x=290, y=275, height=25)

        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()