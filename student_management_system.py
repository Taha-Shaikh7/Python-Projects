import pandas as pd
student=[
    ("student1",19,90),
    ("student2",23,89)
]
student=pd.DataFrame(student,columns=["name","age","marks"])
print("Student management system")
print("1.Add a student")
print("2.Delete the student")
print("3.Search student")
print("4.Update student")
choice=int(input("Enter the choice: "))
if choice==1:
    name=input("Enter name: ")
    age=int(input("Enter age: "))
    marks=int(input("Enter marks: "))
    student.loc[len(student)]=[name,age,marks]
    print("Added Successfully")

elif choice==2:
    name=input("Enter name: ")
    student = student[student["name"] != name]
    print("Deleted Successfully")

elif choice==3:
    name=input("Enter name: ")
    result=student[student["name"]==name]
    print(result)

elif choice==4:
    old=input("Enter the old name: ")
    name=input("Enter new name: ")
    student.loc[student["name"] == old, "name"]=name

else:
    print("Invalid")

