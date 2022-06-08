from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import tkinter.messagebox
import os
import sqlite3


#####################################################################################################################################################################################

class sis(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        bg = PhotoImage(file=r'''C:\Users\rotsen\Documents\SIS.V2 folder\ohmy.png''')
        all_frame = tk.Frame(self)
        all_frame.pack(side="top", fill="both", expand = True)
        all_frame.rowconfigure(0, weight=1)
        all_frame.columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Students, Home, Courses):
            frame = F(all_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show(Home)
    def show(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

#####################################################################################################################################################################################



def iExit():
            iExit = tkinter.messagebox.askyesno("Student Information System","Are you sure you want to exit?")
            if iExit > 0:
                root.destroy()
                return
            
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="Welcome! to the Student Information System", font=("Times New Roman", 45), bg="pink", fg="black")
        label.place(x=230,y=60)

        home = tk.Button(self, text="HOME",font=("Lucida Console",16,"bold"),bd=0, width = 10, bg="pink", fg="black", command=lambda: controller.show(Home))
        home.place(x=380,y=300)
        home.config(cursor= "hand2")
        
        course = tk.Button(self, text="COURSES",font=("Lucida Console",16,"bold"),bd=0, width = 10, bg="pink", fg="black", command=lambda: controller.show(Courses))
        course.place(x=568,y=300)
        course.config(cursor= "hand2")
        
        students = tk.Button(self, text="REGISTRATION",font=("Lucida Console",16,"bold"),bd=0, width = 13, bg="pink", fg="black", command=lambda: controller.show(Students))
        students.place(x=750,y=300)
        students.config(cursor= "hand2")

        students = tk.Button(self, text="EXIT",font=("Lucida Console",15,"bold"),bd=0, width = 10, bg="pink", fg="black", command=iExit)
        students.place(x=1000,y=300)
        students.config(cursor= "hand2")

        
        
  #####################################################################################################################################################################################      

class Courses(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("SIS.V2")
        
        label = tk.Label(self, text="COURSES", font=("Garamond", 40))
        label.place(x=130,y=20)
        
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def tablec():
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def add_course():
            if Course_Code.get() == "" or Course_Name.get() == "" : 
                tkinter.messagebox.showinfo("SIS", "Fill in the box")
            else:
                conn = sqlite3.connect("sis_v2.db")
                c = conn.cursor()         
                c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",(Course_Code.get(),Course_Name.get()))        
                conn.commit()           
                conn.close()
                Course_Code.set('')
                Course_Name.set('') 
                tkinter.messagebox.showinfo("SIS", "Course is Added!")
                display_course()
              
        def display_course():
            self.course_list.delete(*self.course_list.get_children())
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def update_course():
            for selected in self.course_list.selection():
                conn = sqlite3.connect("sis_v2.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", (Course_Code.get(),Course_Name.get(), self.course_list.set(selected, '#1')))  
                conn.commit()
                tkinter.messagebox.showinfo("SIS", "Course is Updated!")
                display_course()
                clear()
                conn.close()
                
        def edit_course():
            x = self.course_list.focus()
            if x == "":
                tkinter.messagebox.showerror("SIS", "Please select a course!")
                return
            values = self.course_list.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def delete_course(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("SIS", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sis_v2.db")
                    cur = con.cursor()
                    x = self.course_list.selection()[0]
                    id_no = self.course_list.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.course_list.delete(x)
                    tkinter.messagebox.showinfo("SIS", "Deleted!")
                    display_course()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("SIS", "This course has students!")
                
        def search_course():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("sis_v2.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.course_list.delete(*self.course_list.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            con.close()

        def iExit():
            iExit = tkinter.messagebox.askyesno(" Student Information System","Are you sure you want to exit")
            if iExit > 0:
                root.destroy()
                return
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):
            item = self.course_list.selection()[0]
            values = self.course_list.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])

        home = tk.Button(self, text="HOME",font=("Lucida Console",13,"bold"),bd=0, width = 10, bg="pink", fg="black", command=lambda: controller.show(Home))
        home.place(x=1,y=35)
        home.config(cursor= "hand2")
        
        

        
        self.lblccode = Label(self, font=("Lucida Console", 12, "bold"), text="Course Code:", padx=5, pady=5)
        self.lblccode.place(x=125,y=144)
        self.txtccode = Entry(self, font=("Lucida Console", 13), textvariable=Course_Code, width=31)
        self.txtccode.place(x=270,y=150)

        self.lblcname = Label(self, font=("Lucida Console", 12,"bold"), text="Course Name:", padx=5, pady=5)
        self.lblcname.place(x=125,y=205)
        self.txtcname = Entry(self, font=("Lucida Console", 13), textvariable=Course_Name, width=31)
        self.txtcname.place(x=270,y=210)
        
        self.SearchBar = Entry(self, font=("Lucida Console", 11), textvariable=SearchBar_Var, bd=0,bg="light pink",width=31)
        self.SearchBar.place(x=876,y=100)
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1215,y=140,height=390)

        self.course_list = ttk.Treeview(self, columns=("Course Code","Course Name"), height = 18, yscrollcommand=scrollbar.set)

        self.course_list.heading("Course Code", text="Course Code", anchor=W)
        self.course_list.heading("Course Name", text="Course Name",anchor=W)
        self.course_list['show'] = 'headings'

        self.course_list.column("Course Code", width=200, anchor=W, stretch=False)
        self.course_list.column("Course Name", width=430, stretch=False)
        
        self.course_list.bind("<Double-1> ", OnDoubleclick)


        self.course_list.place(x=575,y=140)
        scrollbar.config(command=self.course_list.yview)
            
        ## Buttons

        self.adds = Button(self, text="ADD", font=('Lucida Console', 11, ), height=1, width=10, bd=1, bg="pink", fg="black",command=add_course)
        self.adds.place(x=460,y=300)
        self.adds.config(cursor= "hand2")

        self.update = Button(self, text="UPDATE", font=('Lucida Console', 11), height=1, width=10, bd=1, bg="pink", fg="black", command=update_course) 
        self.update.place(x=460,y=360)
        self.update.config(cursor= "hand2")

        self.clear = Button(self, text="CLEAR", font=('Lucida Console', 11), height=1, width=10, bd=1, bg="pink", fg="black", command=clear)
        self.clear.place(x=460,y=420)
        self.clear.config(cursor= "hand2")

        self.delete = Button(self, text="DELETE", font=('Lucida Console', 11), height=1, width=10, bd=1, bg="pink", fg="black", command=delete_course)
        self.delete.place(x=460,y=480)
        self.delete.config(cursor= "hand2")

        self.search = Button(self, text="SEARCH", font=('Lucida Console', 11, 'bold'),bd=0, bg= "pink", fg="black", command=search_course)
        self.search.place(x=1160,y=100)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="DISPLAY", font=('Lucida Console', 11, 'bold'), height=1, width=11, bg="pink", fg="black", command=display_course)
        self.display.place(x=575,y=105)
        self.display.config(cursor= "hand2")
        
        tablec()
        display_course()

#####################################################################################################################################################################################

class Students(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("SIS.V2")
        
        label = tk.Label(self, text="STUDENT REGISTRATION ", font=("Garamond", 40), bg="pink")
        label.place(x=130,y=20)
        
        home = tk.Button(self, text="HOME",font=("Lucida Console",12,"bold"),bd=0, width = 7, bg="pink", fg="black",  command=lambda: controller.show(Home))
        home.place(x=1,y=35)
        home.config(cursor= "hand2")

       
        
        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()
        

        def tables():
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                      Student_YearLevel TEXT, Student_Gender TEXT, \
                      FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def add_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("SIS", "Fill in the box")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("SIS", "Invalid ID")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("SIS", "Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("sis_v2.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO students(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("SIS", "Student is Added!")
                                    conn.commit() 
                                    clear()
                                    display_stud()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("sis_v2.db")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM students")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    if ID in ids:
                                       tkinter.messagebox.showerror("SIS", "ID already exist")
                                    else: 
                                       tkinter.messagebox.showerror("SIS", "Im sorry Course is Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("SIS", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("SIS", "Invalid ID")
                 
        def update_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("SIS", "Please select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("sis_v2.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE students SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("SIS", "Updated!")
                    display_stud()
                    clear()
                    conn.close()
        
        def delete_stud():   
            try:
                messageDelete = tkinter.messagebox.askyesno("SIS", "Are you sure you want to permanently remove this?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sis_v2.db")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM students WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("SIS", "Deleted!")
                    display_stud()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def search_stud():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("sis_v2.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM students")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Student_ID):
                        self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("SIS", "Invalid ID")           
                
        def display_stud():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def edit_stud():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("SIS", "Please Select a record")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        

        self.lblid = Label(self, font=("Lucida Console", 12,"bold"), text="ID Number:", padx=5, pady=5)
        self.lblid.place(x=125,y=144)
        self.txtid = Entry(self, font=("Lucida Console", 13), textvariable=Student_ID, width=33)
        self.txtid.place(x=255,y=150)

        self.lblname = Label(self, font=("Lucida Console", 12,"bold"), text="Name:", padx=5, pady=5)
        self.lblname.place(x=125,y=205)
        self.txtname = Entry(self, font=("Lucida Console", 13), textvariable=Student_Name, width=33)
        self.txtname.place(x=255,y=210)
        
        self.lblc = Label(self, font=("Lucida Console", 12,"bold"), text="Course Code:", padx=5, pady=5)
        self.lblc.place(x=125,y=269)
        self.txtyear = ttk.Combobox(self, value=["BSSTAT", "ABPOLSCI", "BSCHEM", "BSM", "BSMATH", "BSPSYCH", "BSBIO", "BSSOCIO", "BSCE", "BSIT", "BSE", "BSHM", "BSHIST", "BSN", "BSA", "BSCS"], state="readonly", font=("Lucida Console", 12), textvariable=Course_Code, width=28)
        self.txtyear.place(x=255,y=274)
        

        self.lblyear = Label(self, font=("Lucida Console", 12,"bold"), text="Year Level:", padx=5, pady=5)
        self.lblyear.place(x=125,y=315)
        self.txtyear = ttk.Combobox(self, value=["1st Year", "2nd Year", "3rd Year", "4th Year"], state="readonly", font=("Times New Roman", 13), textvariable=Student_YearLevel, width=31)
        self.txtyear.place(x=255,y=320)
        
        self.lblgender = Label(self, font=("Times New Roman", 13,"bold"), text="Gender:", padx=5, pady=5)
        self.lblgender.place(x=125,y=361)
        self.txtgender = ttk.Combobox(self, value=["Male", "Female"], font=("Lucida Console", 13), state="readonly", textvariable=Student_Gender, width=28)
        self.txtgender.place(x=255,y=366)

        self.SearchBar = Entry(self, font=("Lucida Console", 11), textvariable=SearchBar_Var, bd=0,bg="light pink", width=31)
        self.SearchBar.place(x=876,y=100)

        ## Treeview
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1215,y=140,height=390)

        self.studentlist = ttk.Treeview(self, columns=("ID Number", "Name", "Course", "Year Level", "Gender"), height = 18, yscrollcommand=scrollbar.set)

        self.studentlist.heading("ID Number", text="ID Number", anchor=W)
        self.studentlist.heading("Name", text="Name",anchor=W)
        self.studentlist.heading("Course", text="Course",anchor=W)
        self.studentlist.heading("Year Level", text="Year Level",anchor=W)
        self.studentlist.heading("Gender", text="Gender",anchor=W)
        self.studentlist['show'] = 'headings'

        self.studentlist.column("ID Number", width=100, anchor=W, stretch=False)
        self.studentlist.column("Name", width=200, stretch=False)
        self.studentlist.column("Course", width=130, anchor=W, stretch=False)
        self.studentlist.column("Year Level", width=100, anchor=W, stretch=False)
        self.studentlist.column("Gender", width=100, anchor=W, stretch=False)
        
        self.studentlist.bind("<Double-1>",OnDoubleClick)
        
        

        self.studentlist.place(x=575,y=140)
        scrollbar.config(command=self.studentlist.yview)
        
        ## Buttons
        
        self.add = Button(self, text="ADD", font=('Times New Roman', 11), height=1, width=10, bd=1,  bg="pink", fg="black", command=add_stud)
        self.add.place(x=150,y=420)
        self.add.config(cursor= "hand2")

        self.update = Button(self, text="UPDATE", font=('Times New Roman', 11), height=1, width=10, bd=1, bg="pink", fg="black", command=update_stud)
        self.update.place(x=250,y=420)
        self.update.config(cursor= "hand2")

        self.clear = Button(self, text="CLEAR", font=('Times New Roman', 11), height=1, width=10, bd=1, bg="pink", fg="black", command=clear)
        self.clear.place(x=350,y=420)
        self.clear.config(cursor= "hand2")

        self.delete = Button(self, text="DELETE", font=('Times New Roman', 11), height=1, width=10, bd=1, bg="pink", fg="black", command=delete_stud)
        self.delete.place(x=450,y=420)
        self.delete.config(cursor= "hand2")

        self.search = Button(self, text="SEARCH", font=('Times New Roman', 11, 'bold'),bd=0, bg= 'pink', fg="black", command=search_stud)
        self.search.place(x=1160,y=100)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="DISPLAY", font=('Times New Roman', 11, 'bold'), height=1, width=11,  bg="pink", fg="black",command = display_stud)
        self.display.place(x=575,y=105)
        self.display.config(cursor= "hand2")

        tables()
        display_stud()

#####################################################################################################################################################################################

root = sis()
root.geometry("1350x600")
bg = PhotoImage(file=r'''C:\Users\rotsen\Documents\SIS.V2 folder\ohmy.png''')


root.mainloop()
