from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.ttk as ttk
import csv
import os


class Student:
    
    def __init__ (self,root):
        self.root = root
        blank_space = ""
        self.root.title(200 * blank_space + "Student Information System")
        self.root.geometry("1350x1000")
        self.root.resizable(False,False)
        self.data = dict()
        self.temp = dict()
        self.filename = "studentinfo.csv"
        
        Student_First_Name = StringVar()
        Student_Last_Name = StringVar()
        Student_IDNumber = StringVar()
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Student_Course = StringVar()
        searchbar = StringVar()
        
        if not os.path.exists('studentinfo.csv'):
            with open('studentinfo.csv', mode='w') as csv_file:
                fieldnames = ["Student ID Number", "Last Name", "First Name","Gender", "Year Level", "Course"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
        
        else:
            with open('studentinfo.csv', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.data[row["Student ID Number"]] = {'Last Name': row["Last Name"], 'First Name': row["First Name"], 'Gender': row["Gender"],'Year Level': row["Year Level"], 'Course': row["Course"]}
            self.temp = self.data.copy()
        
        
         
        #=============================================================FUNCTIONS================================================================#
        
        def iExit():
            iExit = tkinter.messagebox.askyesno(" Student Information System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
            
        def addStudent():
            with open('studentinfo.csv', "a", newline="") as file:
                csvfile = csv.writer(file)
                if Student_IDNumber.get()=="" or Student_First_Name.get()=="" or Student_Last_Name.get()=="" or Student_YearLevel.get()=="":
                    tkinter.messagebox.showinfo("SIS","Please fill in the box.")
                else:
                    self.data[Student_IDNumber.get()] = {'Last Name': Student_Last_Name.get(), 'First Name': Student_First_Name.get(), 'Gender': Student_Gender.get(),'Year Level': Student_YearLevel.get(), 'Course': Student_Course.get()}
                    self.saveData()
                    tkinter.messagebox.showinfo("SIS", "Recorded Successfully!")
                Clear()
                displayData()
                    
        
        def Clear():
            Student_IDNumber.set("")
            Student_First_Name.set("")
            Student_Last_Name.set("")
            Student_YearLevel.set("")
            Student_Gender.set("")
            Student_Course.set("")
        
        
        
        def displayData():
            tree.delete(*tree.get_children())
            with open('studentinfo.csv') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    IDNumber=row['Student ID Number']
                    LastName=row['Last Name']
                    FirstName=row['First Name']
                    YearLevel=row['Year Level']
                    Course=row['Course']
                    Gender=row['Gender']
                    tree.insert("",END, values=(IDNumber, LastName, FirstName, Gender, YearLevel, Course))
                    
      
        
        def deleteData():
            if tree.focus()=="":
                tkinter.messagebox.showerror("Student Information System","Please select a student record from the table")
                return
            id_no = tree.item(tree.focus(),"values")[0]
            
            self.data.pop(id_no, None)
            self.saveData()
            tree.delete(tree.focus())
            tkinter.messagebox.showinfo("Student Information System","Student Record Deleted Successfully")
            
        
        
        def searchData():
            if self.searchbar.get() in self.data:
                vals = list(self.data[self.searchbar.get()].values())
                tree.delete(*tree.get_children())
                tree.insert("",0, values=(self.searchbar.get(), vals[0],vals[1],vals[2],vals[3],vals[4],vals[5]))
            elif self.searchbar.get() == "":
                displayData()
            else:
                tkinter.messagebox.showerror("Student Information System","Student not found!")
                return
            
        
        
        
        def editData():
            if tree.focus() == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a student record from the table")
                return
            values = tree.item(tree.focus(), "values")
            Student_IDNumber.set(values[0])
            Student_Last_Name.set(values[1])
            Student_First_Name.set(values[2])
            Student_Gender.set(values[3])
            Student_YearLevel.set(values[4])
            Student_Course.set(values[5])
       
    
       
        def updateData():
            with open('studentinfo.csv', "a", newline="") as file:
                csvfile = csv.writer(file)
                if Student_IDNumber.get()=="" or Student_First_Name.get()=="" or Student_Last_Name.get()=="" or Student_YearLevel.get()=="":
                    tkinter.messagebox.showinfo("SIS","Please select a student record from the table")
                else:
                    self.data[Student_IDNumber.get()] = {'Last Name': Student_Last_Name.get(), 'First Name': Student_First_Name.get(), 'Gender': Student_Gender.get(),'Year Level': Student_YearLevel.get(), 'Course': Student_Course.get()}
                    self.saveData()
                    tkinter.messagebox.showinfo("SIS", "Updated")
                Clear()
                displayData()     

        #============================================================FRAMES====================================================#
        
        MainFrame = Frame(self.root, bd=7, width=1000, height=1000, relief=RIDGE, bg="light pink")
        MainFrame.grid()
        
        TopFrame1 = Frame(MainFrame,  width=1330, height=130, relief=RIDGE,bg="gray")
        TopFrame1.grid(row=2, column=0)
        
        TitleFrame = Frame(MainFrame, bg="light pink",bd=5, width=1340, height=100, relief=RIDGE)
        TitleFrame.grid(row=0, column=0)
        
        TopFrame2 = Frame(MainFrame, bd=5,bg="black", width=1340, height=450, relief=RIDGE)
        TopFrame2.grid(row=1, column=0)
        
        SearchFrame = Frame(MainFrame, width = 1340, height = 100, relief = RIDGE)
        SearchFrame.grid(row =3, column =0)
        
        LeftFrame = Frame(TopFrame2, bd=5, width=1350, height=400, padx=2, bg="hot pink", relief=RIDGE)
        LeftFrame.pack(side=LEFT)
        
        LeftFrame1 = Frame(LeftFrame, bd=5,bg="gray", width=600, height=600, padx=4, pady=4, relief=RIDGE)
        LeftFrame1.pack(side=TOP, padx=0, pady=0)
        
        RightFrame1 = Frame(TopFrame2, bd=5, width=600, height=400, padx=2, bg="light pink", relief=RIDGE)
        RightFrame1.pack(side=RIGHT)

        
        
        #=============================================TITLE===========================================#
        
        self.lblTitle = Label(TitleFrame, font=('Garamond',40,'bold'), text="STUDENT INFORMATION SYSTEM", bg="light pink",bd=7)
        self.lblTitle.grid(row=0, column=0, padx=135)
        
        #===========================================================================LABELS & ENTRy WIDGETS=======================================================#
        
        
        self.lblStudentID = Label(RightFrame1, font=('Garamond',12,'bold'), text="STUDENT ID NUMBER:",bg="light pink", bd=5 , anchor=W)
        self.lblStudentID.grid(row=0, column=0, sticky=W, padx=5)
        self.txtStudentID = Entry(RightFrame1, font=('Garamond',12,'bold'), width=40, justify='left', textvariable = Student_IDNumber)
        self.txtStudentID.grid(row=0, column=1)
        
        self.lblLastName = Label(RightFrame1, font=('Garamond',12,'bold'), text="LAST NAME:",bg="light pink",bd=7, anchor=W)
        self.lblLastName.grid(row=1, column=0, sticky=W, padx=5)
        self.txtLastName = Entry(RightFrame1, font=('Garamond',12,'bold'), width=40, justify='left', textvariable = Student_Last_Name)
        self.txtLastName.grid(row=1, column=1)
        
        self.lblFirstName = Label(RightFrame1, font=('Garamond',12,'bold'), text="FIRST NAME:",bg="light pink", bd=7, anchor=W)
        self.lblFirstName.grid(row=2, column=0, sticky=W, padx=5)
        self.txtFirstName = Entry(RightFrame1, font=('Garamond',12,'bold'), width=40, justify='left', textvariable = Student_First_Name)
        self.txtFirstName.grid(row=2, column=1)
        
        
        self.lblCourse = Label(RightFrame1, font=('Garamond',12,'bold'), text="COURSE:",bg="light pink", bd=7, anchor=W)
        self.lblCourse.grid(row=4, column=0, sticky=W, padx=5)
        self.txtCourse = Entry(RightFrame1, font=('Garamond',12,'bold'), width=40, justify='left', textvariable = Student_Course)
        self.txtCourse.grid(row=4, column=1)
        
        self.lblGender = Label(RightFrame1, font=('Garamond',12,'bold'), text="GENDER:", bg="light pink",bd=7, anchor=W)
        self.lblGender.grid(row=5, column=0, sticky=W, padx=5)
        
        self.cboGender = ttk.Combobox(RightFrame1, font=('Garamond',12,'bold'), state='readonly', width=39, textvariable = Student_Gender)
        self.cboGender['values'] = ('Female', 'Male')
        self.cboGender.grid(row=5, column=1)
        
        self.lblYearLevel = Label(RightFrame1, font=('Garamond',12,'bold'), text="YEAR LEVEL:", bg="light pink",bd=7, anchor=W)
        self.lblYearLevel.grid(row=6, column=0, sticky=W, padx=5)
        
        self.cboYearLevel = ttk.Combobox(RightFrame1, font=('Garamond',12,'bold'), state='readonly', width=39, textvariable = Student_YearLevel)
        self.cboYearLevel['values'] = ('1st Year', '2nd Year', '3rd Year', '4th Year')
        self.cboYearLevel.grid(row=6, column=1)
        
        self.searchbar = Entry(self.root, font=('Garamond',12,'bold'), textvariable = searchbar, width = 29 )
        self.searchbar.place(x=900,y=480)
        
        
        
        
        #=========================================================BUTTONS================================================#
        
        self.btnAddNew=Button(self.root, pady=1,bd=4,font=('Garamond',16,'bold'), padx=12, width=8,fg="black", text='ADD',bg="light pink", command=addStudent)
        self.btnAddNew.place(x=50,y=519)
        
        self.btnClear=Button(self.root, pady=1,bd=4,font=('Garamond',16,'bold'), padx=2, width=8,fg="black", text='CLEAR',bg="light pink", command=Clear)
        self.btnClear.place(x=195,y=519)
        
        self.btnUpdate=Button(self.root, pady=1,bd=4,font=('Garamond',16,'bold'), padx=2, width=8,fg="black", text='UPDATE',bg="light pink", command=updateData)
        self.btnUpdate.place(x=570,y=520)

        self.btnEdit=Button(self.root, pady=1,bd=4,font=('Garamond',16,'bold'), padx=2, width=8,fg="black", text='EDIT',bg="light pink", command = editData)
        self.btnEdit.place(x=445,y=520)

        self.btnDisplay=Button(self.root, pady=1,bd=4, font=('Garamond', 16, 'bold'),padx=2,width=8, fg="black",text="DISPLAY" ,bg="light pink", command=displayData)
        self.btnDisplay.place(x=320,y=520)


        self.btnDelete=Button(self.root, pady=1,bd=4,font=('Garamond',16,'bold'), padx=2, width=8,fg="black", text='DELETE',bg="light pink", command = deleteData)
        self.btnDelete.place(x=700,y=520)

        self.btnExit=Button(self.root, pady=1,bd=4,font=('Garamond',16,'bold'), padx=2, width=8,fg="black", text='EXIT',bg="light pink", command = iExit)
        self.btnExit.place(x=820,y=520)

        self.btnSearch=Button(self.root, pady=1,bd=4,font=('Garamond',11,'bold'), padx=2, width=18, text='Search by IDNumber',bg="light pink", command = searchData)
        self.btnSearch.place(x=1150,y=480)

        
        
        #==============================================================================TREEVIEW=========================================================================#
        
        scroll_y=Scrollbar(LeftFrame1, orient=VERTICAL)
        
        tree = ttk.Treeview(LeftFrame1, height=15, columns=("Student ID Number", "Last Name", "First Name", "Gender", "Year Level", "Course"), yscrollcommand=scroll_y.set)

        scroll_y.pack(side=LEFT, fill=Y)

        #configure scrollbar
        scroll_y.config(command=tree.yview)

        tree.heading("Student ID Number", text="Student ID Number")
        tree.heading("Last Name", text="Last Name")
        tree.heading("First Name", text="First Name")
        tree.heading("Gender", text="Gender")
        tree.heading("Year Level", text="Year Level")
        tree.heading("Course", text="Course")
        tree['show'] = 'headings'

        tree.column("Student ID Number", width=120)
        tree.column("Last Name", width=100)
        tree.column("First Name", width=100)
        tree.column("Gender", width=70)
        tree.column("Year Level", width=70)
        tree.column("Course", width=80)
        tree.pack(fill=BOTH,expand=1)
        
        displayData()
        #===========================================================================================================================================================#
    def saveData(self):
        temps = []
        with open('studentinfo.csv', "w", newline ='') as update:
            fieldnames = ["Student ID Number","Last Name","First Name","Gender","Year Level","Course"]
            writer = csv.DictWriter(update, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for id, val in self.data.items():
                temp ={"Student ID Number": id}
                for key, value in val.items():
                    temp[key] = value
                temps.append(temp)
            writer.writerows(temps)


if __name__ =='__main__':
    root = Tk()
    application = Student(root)
    root.mainloop()
