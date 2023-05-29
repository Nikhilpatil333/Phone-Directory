
import mysql.connector as m
from mysql.connector import IntegrityError
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
from tkinter import *
from tkinter import messagebox,PhotoImage
from tkinter import ttk
import tkinter as tk


# SQL Connection
mydatabase = m.connect(
    host="localhost",
    user="root",
    password="#Ninetailedredfox33",
    database="phonenumber"
)

query = "INSERT INTO phnumber (Name,Phone_Number,Mobile_Carrier, Geo_Location, Time_Zone, Valid_User) VALUES (%s,%s,%s,%s,%s,%s)"

def contact():
    name=nameEntry.get() #input("Enter Name : ")
    number =numberEntry.get()  # input("Enter Number with +91: ")
    if len(name)==0:
        messagebox.showinfo("Error","Enter Name")
    elif len(number)!=13:
        messagebox.showinfo("Error","Invalid Contact Number")
    else:
        phone = phonenumbers.parse(number)
        time = timezone.time_zones_for_number(phone)
        car = carrier.name_for_number(phone, "en")
        reg = geocoder.description_for_number(phone, "en")
        valid = phonenumbers.is_valid_number(phone)

        cursor = mydatabase.cursor()
        try:
            cursor.execute(query,[str(name),str(phone),car, reg,str(time),str(valid)])
            mydatabase.commit()
            messagebox.showinfo("Successfully","Contact Details Added")
        except IntegrityError:
            messagebox.showinfo("Duplicate Entry.","Phone Number Already Exists.")
        
        
    # to delete the Entered data
    nameEntry.delete(0,END)
    numberEntry.delete(3,END)
   
    

# FONT
# myfontBOLD=font.Font(family='BOLD')

# Window
window=Tk()
window.title("Phone Directory")
window.iconbitmap(r"D:\\DBDA\\Python Programming\\PROJECT\\phonebookicon.ico")
window.config(bg='steel blue')
window.geometry("620x420")

# Name Label and Name Entry Box
nameLabel=Label(window,text="Name : ",font=('Felix Titling',14,'bold'),bg='steel blue')
nameLabel.grid(row=1,column=2,padx=20,pady=20)
nameEntry=Entry(window,width=42,borderwidth=5,background='lemon chiffon')
nameEntry.grid(row=1,column=3,padx=20,pady=10)

# ph Number Label and ph Number Box 
numberLabel=Label(window,text="Enter Phone Number : ",font=('Felix Titling',14,'bold'),bg='steel blue')
numberLabel.grid(row=2,column=2,padx=20,pady=20)
numberEntry=Entry(window,width=42,borderwidth=5,background='lemon chiffon')
numberEntry.grid(row=2,column=3,padx=20,pady=20)
numberEntry.insert(0,"+91")


# Add Contact Button
contactbutton=Button(window,text="Add Contact",bg='CadetBlue1',fg='black',activebackground='green',font=('Copperplate Gothic Bold',14),command=contact)
contactbutton.grid(row=3,column=3,padx=80,pady=10)


# Add Image
logo=PhotoImage(file="D:\\DBDA\\Python Programming\\PROJECT\\phone-book.png")
logo_label=Label(window,image=logo)
logo_label.grid(row=0,column=1,columnspan=4,pady=10)
logo_label.config(bg='steel blue')


# Fetch Data

def showdata():

    # Mysql database connection to show all records
    query1="select Name,Phone_Number,Mobile_Carrier,Geo_Location from phnumber order by Name"
    cursor=mydatabase.cursor()
    cursor.execute(query1)



    # Display Table
    display_records=Toplevel()
    display_records.title("Contact Details : ")
    display_records.iconbitmap(r"D:\\DBDA\\Python Programming\\PROJECT\\phonebookicon.ico")
    display_records.geometry("1000x450")
    display_records.configure(bg='steel blue')

    # TreeView widget
    tree = ttk.Treeview(display_records)
    tree["show"]="headings"

    style=ttk.Style()
    style.theme_use('winnative')
    style.configure('Treeview',rowheight=30,font=('Courier New Baltic',11),fieldbackground='lemon chiffon',background='lemon chiffon')
    # style.configure('tree.heading',foreground='blue',font=('Helvetica',32))
    

    # Define Numbers of columns
    tree['column']=("Name","Phone_Number","Mobile_Carrier","Geo_Location")

    # Assign the width, minwidth and anchor to the respective columns
    tree.column("Name",width=200,minwidth=200,anchor=tk.CENTER)
    tree.column("Phone_Number",width=400,minwidth=400,anchor=tk.CENTER)
    tree.column("Mobile_Carrier",width=200,minwidth=200,anchor=tk.CENTER)
    tree.column("Geo_Location",width=200,minwidth=200,anchor=tk.CENTER)

    # Assign the Heading names to the respective column

    tree.heading("Name",text='NAME',anchor=tk.CENTER)
    tree.heading("Phone_Number",text='PHONE  NUMBER',anchor=tk.CENTER)
    tree.heading("Mobile_Carrier",text='CARRIER  NAME',anchor=tk.CENTER)
    tree.heading("Geo_Location",text='GEO  LOCATION',anchor=tk.CENTER)

    i=0
    for ro in cursor:
        tree.insert('',i, text="",values=(ro[0],ro[1],ro[2],ro[3]))
        i+=1
    
    

    def delete(tree):
        selected_item=tree.selection()[0]
        name=tree.item(selected_item)['values'][0]
        del_query="delete from phnumber where Name=%s"
        select_data=(name,)
        cursor.execute(del_query,select_data)
        mydatabase.commit()
        tree.delete(selected_item)
        messagebox.showinfo("Successful","Contact Deleted Successfully")

    deletebutton=Button(display_records,text='DELETE',bg='red',fg='black',activebackground='green',font=('Times',16,'bold'),command=lambda:delete(tree))
    deletebutton.place(x=450,y=350)


    # to place the tree in widget
    tree.pack()

    display_records.mainloop()

    
# Show All Contacts Button
show_contactbutton=Button(window,text="Show All Contacts",bg='CadetBlue1',fg='black',activebackground='green',font=('Copperplate Gothic Bold',14),command=showdata)
show_contactbutton.grid(row=4,column=3,padx=40,pady=0)



window.mainloop()