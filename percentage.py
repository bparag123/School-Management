from tkinter import *
from tkinter import  messagebox
import sqlite3
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
import json
from reportlab.pdfgen import canvas
import os
import webbrowser

class Percentage(Toplevel):

    def backf(self, event=""):
        self.destroy()
        self.root.deiconify()

    def c_w(self, event=""):
        m = messagebox.askyesno("School Software", "Are you Want to Close Application?", parent=self.root)
        if m > 0:
            self.main_root.destroy()
        else:
            return
    
    def get_data_for_preview_and_result(self):
        return_value = True
        query = "select data from exams"
        j_data = self.conn.execute(query).fetchone()
        self.data = json.loads(j_data[0])
        self.subject = self.data[self.cb1.get()]

        get_std_from_table_name = str(self.subject[-1])
        self.get_std_list = get_std_from_table_name.split("_")

        query = "select count(*) from master where standard = '{}'".format((self.get_std_list[1]))
        self.roll_from_master = self.conn.execute(query).fetchone()
        query = "select count(*) from '{}' where std = '{}'".format(self.subject[-1], (self.get_std_list[1]))
        self.roll_from_result = self.conn.execute(query).fetchone()

        if self.roll_from_master[0] == self.roll_from_result[0]:
           
            query = "select marks from exams"
            fetched_total = self.conn.execute(query).fetchone()
            self.mark = json.loads(fetched_total[0])
            self.mark_list = self.mark[self.cb1.get()]
            self.total_exam_mark = 0
            for i in self.mark_list:
                self.total_exam_mark += int(i)
            query = "select * from '{}' order by rollno".format(self.subject[-1])
            self.all_details_marks = self.conn.execute(query).fetchall()
            query = "select * from master where standard = '{}' order by rollno".format((self.get_std_list[1]))
            self.all_details_student = self.conn.execute(query).fetchall()

            return_value = True

        else:
            messagebox.showerror("School Software",
                                 "Mark Entry of All Students for Exam '{}' is not Done.".format(self.cb1.get()))
            self.cb1.set("Select")
            return_value = False

        if self.roll_from_master[0] < int(self.rank_var.get()):
            messagebox.showerror("School Software",
                                 "Total {} Students Appeared for Exam : {}.\nYou want give Rank to The {} Students.\nWhich is Impossible.\nPlease Correct It.".format(self.roll_from_master[0], self.cb1.get(), self.rank_var.get()))
            self.cb1.set("Select")
            self.rank.focus_set()
            return_value = False
        
        return return_value
        
    def selected_exam(self,event):
        
        if self.examname_var.get() == "":
            messagebox.showerror("School Software", "Please Enter Exam Title..")
            self.examname.focus_set()
            return

        if self.rank.get() == "":
            messagebox.showerror("School Software", "Please Enter Rank..")
            self.rank.focus_set()
            return
        try:
            r = int(self.rank.get())
            if r < 1:
                messagebox.showerror("School Software", "Please Enter Valid Rank. Rank Should Be Positive Number.")
                self.rank.focus_set()
                return
        except:
            messagebox.showerror("School Software", "Please Enter Valid Rank. Rank Should Be Positive Number.")
            self.rank.focus_set()
            return
        
        get_return_value = self.get_data_for_preview_and_result()
        if not get_return_value:
            return

        self.preview_btn = Button(self.lf2, text="See Preview", command=self.preview)
        self.preview_btn.place(x=300, y=450, height=25)
        self.generate_btn = Button(self.lf2, text="Generate Result", command=self.generate_result)
        self.generate_btn.place(x=600, y=450, height=25)

    def preview(self):
        pdf = canvas.Canvas("C:\\Reports\\Exams\\preview_{}.pdf".format(self.cb1.get()))
        pdf.setPageSize((600, 930))
        pdf.line(10, 800, 590, 800)

        length_cols = len(self.all_details_marks)
        length_rows = len(self.all_details_marks[0])
        diff = int(550 / (length_rows - 1))

        pdf.setFont("Courier-Bold", 15)
        heading = self.cb1.get().split("_")

        pdf.drawString(50, 890, "Preview Report : {}".format(self.examname_var.get()))
        pdf.drawString(50, 870, "Standard : {}".format(heading[1]))
        pdf.drawString(430, 870, "Date : {}".format(heading[2]))

        side = 40
        
        pdf.setFont("Courier-Bold", 12)
        head_side = 30
        pdf.drawString(head_side, 820, "Roll")
        head_side += diff
        pdf.line(10, 835, 590 , 835)
        for i in range(len(self.subject) - 1):
            if i % 2 == 0:
                pdf.drawString(head_side, 825, self.subject[i])
            else:
                pdf.drawString((head_side + 10), 820, "Int.")
            pdf.drawString((side + diff), 805, '({})'.format(self.mark_list[i]))
            side += diff
            head_side += diff
        pdf.setFont("Courier-Bold", 12)
        side = 50
        top = 780
        for i in range(length_cols):
            if top < 30:
                pdf.showPage()
                top = 850
                side = 50
            for j in range(1, length_rows):
                pdf.drawString(side, top, "{}".format(self.all_details_marks[i][j]))
                side += diff
            top -= 15
            side = 50

        pdf.save()
        messagebox.showinfo("School Software",
                            "Your Preview for Exam '{}' is Generated Succesfully !\n".format(self.cb1.get()))
        webbrowser.open("C:\\Reports\\Exams\\report_{}.pdf".format(self.cb1.get()))
    
    def generate_result(self):
        m = messagebox.askyesnocancel("School Software", "Before Generating Result Please Ensure that you have Entered Correct Marks for all Students, After Generating Result you can't Update Marks.\nFor Mark Details Please See Preview.\nAre You really Want to Generate Result of Exam : '{}' ?".format(self.cb1.get()))
        if m == True:

            os.makedirs("C:\\Results\\{}".format(self.cb1.get()))
            get_return_value = self.get_data_for_preview_and_result()
            if get_return_value:
                percentage = []
                self.obtained = []
                self.got = 0
                query = "alter table '{}' add percentage NUMERIC;".format(self.subject[-1])
                self.conn.execute(query)
                self.conn.commit()

                for i in self.all_details_marks:
                    for j in range(2,len(i)):
                        self.got += i[j]
                    per = float((self.got*100)/self.total_exam_mark)
                    percentage.append(per)
                    self.obtained.append(self.got)
                    query = "update '{}' set percentage={} where rollno = {}".format(self.subject[-1], per, i[1])
                    self.conn.execute(query)
                    self.got = 0
                    self.conn.commit()
                #====================
                self.set_percentage = set(percentage)
                #====================
                self.collect_data()
                self.result_pdf()
                self.report_pdf()
                del self.data[self.cb1.get()]
                del self.mark[self.cb1.get()]

                j_mark = json.dumps(self.mark)
                j_data = json.dumps(self.data)
                query = """update exams set data=(?), marks=(?)"""
                self.conn.execute(query, (j_data, j_mark))
                self.conn.commit()

                query = "drop table '{}'".format(self.subject[-1])
                self.conn.execute(query)
                self.conn.commit()
                self.combo_maintain()
                messagebox.showinfo("School Software","Your Result for Exam '{}' is Generated Succesfully !".format(self.cb1.get()))

                self.preview_btn.destroy()
                self.generate_btn.destroy()
                self.cb1.set("Select")
                self.examname_var.set('')
                self.rank_var.set('')
            else:
                return
        elif m == False:
            self.combo_var.set('Select')
            self.preview_btn.destroy()
            self.generate_btn.destroy()
            return
        else:
            return

    def collect_data(self):
        query = "select * from '{}' order by rollno".format(self.subject[-1])
        self.all_details_marks = self.conn.execute(query).fetchall()
        query = "select grno,rollno,standard,fname,mname,lname from master where standard = '{}' order by rollno".format((self.get_std_list[1]))
        self.all_details_student = self.conn.execute(query).fetchall()
        self.ranks = list(self.set_percentage)
        self.ranks.sort()
        self.ranks.reverse()
        self.rank_list = []
        for i in range(int(self.rank.get())):
            self.rank_list.append(round(self.ranks[i], 2))
        print(self.rank_list)
    
    def combo_maintain(self):
        query = "select data from exams"
        j_data = self.conn.execute(query).fetchone()
        data = json.loads(j_data[0])
        exams = data.keys()
        k = []
        for i in exams:
            k.append(i)
        self.cb1['values'] = k

    def report_pdf(self):
        pdf = canvas.Canvas("C:\\Reports\\Exams\\{}.pdf".format(self.cb1.get()))
        pdf.setPageSize((600, 930))
        pdf.line(10, 800, 590, 800)
        pdf.line(10, 835, 590 , 835)

        length_cols = len(self.all_details_marks)
        length_rows = len(self.all_details_marks[0])
        diff = int(550/(length_rows-1))

        pdf.setFont("Courier-Bold", 15)
        heading = self.cb1.get().split("_")

        pdf.drawString(50, 890, "Exam Report : {}".format(self.examname_var.get()))
        pdf.drawString(50, 870, "Standard : {}".format(heading[1]))
        pdf.drawString(430, 870, "Date : {}".format(heading[2]))

        side = 40
        
        pdf.setFont("Courier-Bold", 12)
        head_side = 30
        pdf.drawString(head_side,820,"Roll")
        head_side += diff
        pdf.setFont("Courier-Bold", 10)
        for i in range(len(self.subject)-1):
            if i%2 ==0:
                pdf.drawString(head_side,825,self.subject[i])
            else:
                pdf.drawString((head_side+10),820,"Int.")
            pdf.drawString((side+diff),805,'({})'.format(self.mark_list[i]))
            side += diff
            head_side += diff
        pdf.drawString(head_side, 825, "Percentage")
        pdf.setFont("Courier-Bold", 12)
        side = 50
        top = 780
        for i in range(length_cols):
            if top < 30:
                pdf.showPage()
                top = 850
                side = 50

            for j in range(1, length_rows):
                pdf.drawString(side, top, "{}".format(self.all_details_marks[i][j]))
                side += diff
            top -= 15
            side = 50
        pdf.save()
    
    def result_pdf(self):
        for i in range(len(self.all_details_marks)):

            pdf = canvas.Canvas("C:\\Results\\{}\\result_{}_{}.pdf".format(self.cb1.get(),self.all_details_student[i][2],self.all_details_student[i][1]))
            pdf.setFillColor('#F9F280')
            pdf.setPageSize((600, 900))
            pdf.rect(0, 0, 600, 900, fill=1)
            pdf.setFillColor('#4D722E')

            pdf.line(10, 600, 10, 200)
            pdf.line(580, 600, 580, 200)
            pdf.line(10, 200, 580, 200)

            pdf.line(10, 570, 580, 570)
            pdf.line(10, 600, 580, 600)
            pdf.line(50, 600, 50, 200)
            pdf.line(530, 600, 530, 200)
            pdf.line(480, 600, 480, 200)
            pdf.line(430, 600, 430, 200)
            pdf.line(380, 600, 380, 200)
            pdf.line(330, 600, 330, 200)
            pdf.line(280, 600, 280, 200)

            pdf.line(10, 725, 10, 825)
            pdf.line(150, 725, 150, 825)
            pdf.line(10, 725, 150, 725)
            pdf.line(10, 825, 150, 825)

            logo = 'logo.jpg'
            pdf.drawInlineImage(logo, 30, 725)

            pdf.setFont("Courier-Bold", 30)
            pdf.drawString(225, 800, "SCHOOL NAME")

            pdf.setFont("Courier-Bold", 25)
            pdf.drawString(250, 750, str(self.examname_var.get()))

            pdf.setFont("Courier-Bold", 10)
            pdf.drawString(15, 580, "Sr No.")
            pdf.drawString(130, 580, "Subjects")
            pdf.drawString(289, 587, " Exam")
            pdf.drawString(286, 577, "(Total)")
            pdf.drawString(335, 587, " Exam")
            pdf.drawString(330, 577, " (obt.)")
            pdf.drawString(381, 587, "Internal")
            pdf.drawString(381, 577, " (Total)")
            pdf.drawString(431, 587, "Internal")
            pdf.drawString(431, 577, " (obt.)")
            pdf.drawString(488, 587, "TOTAL")
            pdf.drawString(488, 577, "MARKS")
            pdf.drawString(531, 587, "OBTAINED")
            pdf.drawString(538, 577, "MARKS")

            pdf.setFont("Courier-Bold", 12)

            pdf.line(10, 700, 580, 700)
            pdf.line(10, 620, 580, 620)
            pdf.line(20, 610, 20, 710)
            pdf.line(570, 610, 570, 710)

            pdf.line(10, 120, 580, 120)
            pdf.line(10, 170, 580, 170)
            pdf.line(20, 110, 20, 180)
            pdf.line(570, 110, 570, 180)

            pdf.line(460, 40, 580, 40)
            pdf.drawString(450, 20, "Principal Signature")

            #==================================================

            pdf.drawString(60, 680, "Student Name : {} {} {}".format( self.all_details_student[i][3], self.all_details_student[i][4], self.all_details_student[i][5] ))
            pdf.drawString(60, 665, "Standard : {}".format(self.all_details_student[i][2]))
            pdf.drawString(60, 650, "Gr. No. : {}".format(self.all_details_student[i][0]))
            pdf.drawString(60, 635, "Roll No. : {}".format(self.all_details_student[i][1]))

            result = True
            #=========Fetching Marks==================================

            top = 500
            sr = 1
            for j in range(0,len(self.subject)-1,2):
                pdf.drawString(130,top,str(self.subject[j]))
                pdf.drawString(30, top,str(sr))
                sr += 1
                top -= 25
            top_e_m = 500
            top_i_m = 500
            subject_total = []

            #this is mark calculation counter for subject total
            x = 0
            for j in range(len(self.mark_list)):
                if j%2 ==0 :
                    pdf.drawString(293, top_e_m, str(self.mark_list[j]))
                    top_e_m -= 25
                    x += int(self.mark_list[j])
                else:
                    pdf.drawString(389, top_i_m, str(self.mark_list[j]))
                    top_i_m -= 25
                    x += int(self.mark_list[j])
                    subject_total.append(x)
                    x=0
            
            # this is mark calculation counter for obtained
            x = 0
            subject_obtained = []
            top_e_m = 500
            top_i_m = 500
            for j in range(2,len(self.all_details_marks[i])-1):
                if j%2 == 0:
                    pdf.drawString(343, top_e_m, str(self.all_details_marks[i][j]))
                    top_e_m -= 25
                    x += int(self.all_details_marks[i][j])
                    if float(self.all_details_marks[i][j]) < float((int(self.mark_list[j-2])*33)/100):
                        result = False
                else:
                    pdf.drawString(443, top_i_m, str(self.all_details_marks[i][j]))
                    top_i_m -= 25
                    x += int(self.all_details_marks[i][j])
                    subject_obtained.append(x)
                    x = 0

                    if float(self.all_details_marks[i][j]) < float((int(self.mark_list[j-2])*33)/100):
                        result = False
            top = 500

            for j in range(len(subject_obtained)):
                pdf.drawString(490, top, str(subject_total[j]))
                pdf.drawString(540, top, str(subject_obtained[j]))
                top -= 25

            

            pdf.drawString(60, 125, "TOTAL : {}  / {}".format(self.obtained[i], self.total_exam_mark))
            pdf.drawString(60, 155, "Percentage : {}".format(round(float(self.all_details_marks[i][-1]),2)))
            if result:
                pdf.drawString(450, 155, "Result : PASS")
            else:
                pdf.drawString(450, 155, "Result : FAIL")

            try:
                rank = self.rank_list.index(round(self.all_details_marks[i][-1]))
                pdf.drawString(60, 140, "Rank : {}".format(str(rank + 1)))

            except:
                pdf.drawString(60, 140, "Rank : NA")
            #===========================================
            pdf.save()



    def __init__(self, root, main_root):

        self.main_root = main_root
        self.root = root
        Toplevel.__init__(self)
        try:
            self.conn = sqlite3.connect('sinfo.db')
        except:
            messagebox.showerror("School", "Database Problem")
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.bgclr1 = "#0080c0"
        self.bgclr2 = "#e7d95a"
        self.f1 = "Arial Bold"
        self.f2 = "times new roman"
        self.title("Genrate Result ")
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
        self.lf2 = LabelFrame(self, text="Percentage", bd=2, bg="black", fg="white", font=(self.f1, 20), relief=GROOVE)
        self.lf2.place(x=0, y=150, height=550, width=1350)


        #=======================CHanges==================================

        exam_label = Label(self.lf2,text="Exam Name")
        rank_label = Label(self.lf2,text="Enter Total Number Of Ranks, Which You want to give")
        self.examname_var = StringVar()
        self.rank_var = StringVar()
        self.examname = Entry(self.lf2, textvariable=self.examname_var)
        self.rank = Entry(self.lf2, textvariable=self.rank_var)
        exam_label.place(x=200, y=200)
        rank_label.place(x=200, y=300)
        self.examname.place(x=700, y=200)
        self.rank.place(x=700, y=300)

        #=======================CHanges==================================

        self.combo_var = StringVar()
        self.cb1 = Combobox(self.lf2, state="readonly", textvariable=self.combo_var, font=("Arial Bold", 15))
        self.cb1.pack()
        query = "select data from exams"
        j_data = self.conn.execute(query).fetchone()
        data = json.loads(j_data[0])
        exams = data.keys()
        k = []
        for i in exams:
            k.append(i)
        self.cb1['values'] = k
        self.cb1.bind("<<ComboboxSelected>>", self.selected_exam)
        self.cb1.set("Select")


        self.protocol("WM_DELETE_WINDOW", self.c_w)
        self.mainloop()