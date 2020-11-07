from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
import json

class Update_Mark(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event = ""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return

    def set_mark(self):

        m = messagebox.askyesnocancel("School Software","Are you really want to Save the Changes?")

        if m == True:

            if self.combo_roll.get() != 'Select':
                pass
            else:
                messagebox.showerror("School Software", "Please Select Roll Number first.")
                self.combo_roll.focus_set()
                return

            for i in range(len(self.subject) - 1):

                try:
                    int(self.mark_ent[i].get())
                except:
                    messagebox.showerror("School Software",
                                         "For Subject '{}' Marks field Should be Positive Number and Not Null.".format(
                                             self.subject[i]))
                    self.mark_ent[i].focus_set()
                    return

                #==========================================================================
                query = "select marks from exams"
                fetched_total = self.conn.execute(query).fetchone()
                j = json.loads(fetched_total[0])
                mark_list = j[self.combo_get_exam_var.get()]
                if int(self.mark_ent[i].get()) > int(mark_list[i]):
                    messagebox.showerror("School Software",
                                         "For Subject '{}' Total Marks are '{}' and you Entered '{}'.\nIt's not Posiible to give marks more then Total.".format(
                                             self.subject[i],mark_list[i],self.mark_ent[i].get()))
                    self.mark_ent[i].focus_set()
                    return
                #==========================================================================

                if self.mark_ent[i].get() == "" or int(self.mark_ent[i].get())<0:
                    messagebox.showerror("School Software","For Subject '{}' Marks field Should be Positive Number and Not Null.".format(self.subject[i]))
                    self.mark_ent[i].focus_set()
                    return


            self.insert_data_list = []
            self.insert_data_list.append(self.standard_entry_var.get())
            self.insert_data_list.append(self.combo_roll.get())
            self.add_query_formatting = "?"
            for i in range(len(self.subject)-1):
                self.insert_data_list.append(self.mark_ent[i].get())
                self.add_query_formatting += ",?"
            self.add_query_formatting += ",?"
            self.insert_data_tuple = tuple(self.insert_data_list)

            query = "delete from '{}' where std='{}' and rollno = '{}' ".format(self.subject[-1],self.get_std_list[1],self.combo_roll.get())
            self.conn.execute(query)

            query = "insert into '{}' values ({})".format(self.subject[-1], self.add_query_formatting)
            self.conn.execute(query, self.insert_data_tuple)
            for i in range(len(self.subject)-1):
                self.var[i].set('')
            self.rollno_maintain()
            self.combo_roll.set('Select')
            self.conn.commit()
            messagebox.showinfo("School Software", "Your Updation of Marks is Succesful!")
        elif m == False:

            self.reset()

        else:
            return

    def reset(self):
        self.combo_get_exam.config(state="normal")
        self.combo_get_exam.config(state="readonly")
        for i in range(len(self.subject)-1):
            self.mark_ent[i].destroy()
            self.mark_label[i].destroy()
        self.confirm_btn.destroy()
        self.reset_btn.destroy()
        self.standard_label.destroy()
        self.standard_entry.destroy()
        self.combo_roll.destroy()
        self.roll.destroy()

    def get_exam_details(self,event):

        self.combo_get_exam.config(state='disabled')
        query = "select data from exams"
        j_data = self.conn.execute(query).fetchone()
        data = json.loads(j_data[0])
        self.subject = data[self.combo_get_exam_var.get()]

        self.standard_label = Label(self.lf2, text="Standard", width=10)
        self.standard_label.place(x=550, y=10)

        self.standard_entry_var = StringVar()
        self.standard_entry = Entry(self.lf2,state="disabled", textvariable=self.standard_entry_var, width=13)
        self.standard_entry.place(x=650, y=10)

        get_std_from_table_name = str(self.subject[-1])
        self.get_std_list = get_std_from_table_name.split("_")

        self.standard_entry_var.set((self.get_std_list[1]))

        self.var = []
        self.mark_ent = []
        self.mark_label = []
        for i in range(len(self.subject)-1):
            self.var.append(str(i))
            self.mark_ent.append(str(i))
            self.mark_label.append(str(i))

        self.roll = Label(self.lf2, text="Roll No. : ")
        self.roll.place(x=800, y=10)

        self.roll_var = StringVar()
        self.combo_roll = Combobox(self.lf2, state="readonly", textvariable=self.roll_var, font=("Arial Bold", 10))
        self.combo_roll.place(x=900, y=10)
        self.combo_roll.bind("<<ComboboxSelected>>", self.set_exist_values)
        self.combo_roll.set("Select")
        self.rollno_maintain()
        top = 75
        side = 300
        for i in range(len(self.subject)-1):
            self.var[i] = StringVar()
            self.mark_label[i] = Label(self.lf2,text=self.subject[i])
            self.mark_ent[i] = Entry(self.lf2, textvariable=self.var[i])
            if i % 2 == 0:
                self.mark_label[i].place(x=side, y=top)
                self.mark_ent[i].place(x=(side+120), y=top)
            else:
                self.mark_label[i].place(x=((2*side) + 50), y=top)
                self.mark_ent[i].place(x=((2*side) + 220), y=top)
                top += 50
        self.confirm_btn= Button(self.lf2,text="Confirm",command=self.set_mark)
        self.confirm_btn.place(x=550, y=425)
        self.reset_btn = Button(self.lf2, text="Reset", command=self.reset)
        self.reset_btn.place(x=650, y=425)

    def set_exist_values(self,event):

        query = "select * from '{}' where std = '{}' and rollno = '{}'".format(self.subject[-1],(self.get_std_list[1]),self.combo_roll.get())
        self.fetch_value = self.conn.execute(query).fetchall()
        for i in range(2,len(self.fetch_value[0])):
            self.var[i-2].set(self.fetch_value[0][i])

    def rollno_maintain(self):
        query = "select rollno from '{}'".format(self.subject[-1])
        self.count= self.conn.execute(query).fetchone()
        if self.count[0] == 0:
            self.combo_roll['values'] = []
        else:

            query = "select rollno from '{}'".format(self.subject[-1])
            self.inserted_roll = self.conn.execute(query).fetchall()
            self.roll_from_result = []
            for i in self.inserted_roll:
                self.roll_from_result.append(i[0])

            self.combo_roll['values'] = self.roll_from_result

    def __init__(self, root, main_root):

        self.main_root = main_root
        self.root = root
        Toplevel.__init__(self)
        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            messagebox.showerror("School Software", "Database Problem")
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.title("UPDATE MARKS")
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

        ##===================================================frame 2====================================================
        self.lf2 = LabelFrame(self, text="UPDATE MARK'S ", bd=2, bg="black", fg="white", font=(self.f1, 20),
                              relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)

        self.combo_get_exam_var = StringVar()
        self.exam_lbl = Label(self.lf2, text="Exam Name : ")
        self.exam_lbl.place(x=200,y=10)
        self.combo_get_exam = Combobox(self.lf2, state="readonly", textvariable=self.combo_get_exam_var,
                                       font=("Arial Bold", 10))
        self.combo_get_exam.place(x=320, y=10)
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
        self.mainloop()