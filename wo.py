from typing import Callable, Optional, Tuple, Union
import customtkinter as ctk
from import_setup import *
import customtkinter as ctk
import tkinter.messagebox as tkmb
import sqlite3
import yagmail
import CTkTable
from datetime import date


global buttoncount
buttoncount = 0

global adminvar
adminvar = 0
#Database creation
db_connection = sqlite3.connect('project.db')
cursor = db_connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        pk INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        teacher TEXT NOT NULL,
        admin TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS resources (
        pk INTEGER PRIMARY KEY NOT NULL,
        rname TEXT NOT NULL UNIQUE,
        rcount INTEGER NOT NULL,
        rmin INTEGER NOT NULL,
        rorder INTEGER

    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        pk INTEGER PRIMARY KEY NOT NULL,
        orname TEXT NOT NULL,
        ocount INTEGER NOT NULL,
        otime TEXT
               
    )
''')
db_connection.commit()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class Main(ctk.CTkTabview):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def add_logintab(self):
        self.name = 'Login'
        self.e_tab = self.add(self.name)

        self.frame = ctk.CTkFrame(self.e_tab)
        self.frame.pack(ipady=20, ipadx=60, expand = True)

        self.label = ctk.CTkLabel(self.frame, text='Enter Username and Password')
        self.label.pack(pady=12, padx=10)

        self.user_entry = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.user_entry.pack(pady=12, padx=10)

        self.user_pass = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.user_pass.pack(pady=6, padx=10)

        self.button = ctk.CTkButton(self.frame, text='Login', command = self.login)
        self.button.pack(pady = 10)

        self.button = ctk.CTkButton(self.e_tab, text = 'Quit', command = quit)
        self.button.pack()


    def trackMenu(self):
        self.delete(self.name)
        self.name = 'Track'
        self.rtm = self.add(self.name)
        global rsearch
        frame = ctk.CTkScrollableFrame(master = self.rtm)
        frame.pack(pady=100,ipady = 100,ipadx=100, expand=False)

        lable = ctk.CTkLabel(master = frame, text = "Enter reasource name")
        lable.pack()
        searchBox = ctk.CTkEntry(master = frame, placeholder_text="Enter Resource name")
        searchBox.pack(pady = 30)

        def search():
            if searchBox.get() != "":
                rsearch = searchBox.get().strip()
                cursor.execute('SELECT * FROM resources WHERE rname = ?', (rsearch,))
                self.result = cursor.fetchone()
                if self.result is not None: 
                    def showinfo():
                        self.delete(self.name)
                        self.name = "Result"
                        self.resulttab = self.add(self.name)
                        info_font = ctk.CTkFont(family = "Arial", weight = 'bold', size = 23)

                        rname = ctk.CTkLabel(master = self.resulttab,text = self.result[1].upper(), font = info_font)
                        rname.pack(pady = 150)

                        frame = ctk.CTkFrame(master = self.resulttab, fg_color= 'white')
                        frame.pack(ipady=20, ipadx=80)
                    
                        rcount = ctk.CTkLabel(master = frame, text = 'Current count: ' + str(self.result[2]), font = info_font, text_color = 'black') 
                        rcount.pack(pady = 20)
                        rcount.update()
                        rmin = ctk.CTkLabel(master = frame, text = 'Minimum count: '+ str(self.result[3]), font = info_font, text_color = 'black')
                        rmin.pack(pady = 20)
                        
                        takeamount = ctk.CTkEntry(master = frame, placeholder_text= 'Enter Amount to take')
                        takeamount.pack()
                        
                        self.orderflag = 0
                        
                        def order():
                            if self.orderflag >0:
                                ordertime = str(date.today)
                                inserted_data = (self.result[1], self.result[4], ordertime)
                                insert_sql = "INSERT INTO orders(orname,ocount,otime) VALUES(?,?,?)"
                                cursor.execute(insert_sql, inserted_data)
                                db_connection.commit()
                                self.orderbutton.destroy()
                                sucess = ctk.CTkLabel(master=frame, text="Successfully sent in order request.")
                                sucess.pack()
                                self.orderflag = 0
                            self.orderbutton.configure(text = "Confirm?", fg_color="red")
                            self.orderflag=+1



                        def take():
                            string = "String"
                            take_amount = takeamount.get()
                            try:
                                take_amount = int(take_amount)
                            except:
                                take_amount = take_amount
                            if type(take_amount) != type(string) and take_amount != "" and take_amount > 0 and take_amount<= self.result[2]:
                                newrcount = self.result[2] - take_amount
                                cursor.execute('UPDATE resources SET rcount = ? WHERE rname = ?',(newrcount, rsearch))
                                db_connection.commit()
                                perm = ctk.CTkLabel(master = frame, text_color='green',text = (f"Amount {str(take_amount)} taken successfully."))
                                perm.pack()
                                self.after(1500,perm.destroy) 


                                if self.result[2]< self.result[3]:
                                    try:
                                        yag = yagmail.SMTP('inventorymanagerbot','feio avya dxhj dcst')

                                        to = ['davis.g@stac.southwark.sch.uk','favisboss@gmail.com']
                                        subject = 'DO NOT RESPOND'
                                        body = (f'''<h3>Hitting Min Level!</h3>
                                            This is an automatic order request, notifying you that the resource <b>{self.result[1]}</b> has reached its minimum.
                                            Please submit an order of minimum <b>{self.result[4]}</b> of this resource.
                                            It currently holds <b>{self.result[2]}</b>.
                                            Again, please submit this order of <b>{self.result[4]}</b>.
                                            
                                            Kind Regards,
                                            <h1><b><i>Inventory Manager</b></i></h1>''')


                                        yag.send(to=to, subject=subject, contents=body)
                                        yag.close()
                                    except:
                                        tkmb.showerror(message = "Establish connection for email to be sent", title = "Lack of Connectivity")
                            else:
                                perm = ctk.CTkLabel(master = frame, text_color='red',text = 'Invalid Input')
                                perm.pack()
                                self.after(1500,perm.destroy)
                            cursor.execute('SELECT * FROM resources WHERE rname = ?', (rsearch,))
                            self.result = cursor.fetchone()
                        self.takebutton = ctk.CTkButton(master = frame, text = "Take", command = take, width=200, height =40)
                        self.takebutton.pack(pady = "20")

                        self.orderbutton = ctk.CTkButton(master=frame, text = "Order", command = order, width=200, height =40)


                        backbutton = ctk.CTkButton(master = self.resulttab, text = "Back", command=self.add_menu)
                        backbutton.pack()
                    showinfo()
                else:
                    noinfo = ctk.CTkLabel(master = self.rtm, text_color='red',text = 'Invalid Input')
                    noinfo.pack()
                    self.after(1500,noinfo.destroy)

        search_button = ctk.CTkButton(master = frame,command=search, text="Search")
        search_button.pack()
        try:    
            tabview = ctk.CTkTabview(master = frame)
            tabview.pack()
            current_stored = tabview.add("Current Stored")

            cursor.execute('SELECT rname FROM resources')
            result = cursor.fetchall()

            table = CTkTable.CTkTable(master = current_stored, values = result)
            table.pack()
        except:
            print("No Resources stored.")

        def goback2menu():
            self.add_menu()
        self.button = ctk.CTkButton(master = self.rtm, text = "Back", command = goback2menu)
        self.button.pack()

    #The following add function switches from the previous stored frame and uses
    def add_menu(self):
        self.delete(self.name)
        self.name = 'Menu'
        self.menutab = self.add(self.name)

        frame = ctk.CTkFrame(master = self.menutab)
        frame.pack(ipady=70, ipadx=80, fill='none', expand=True)

        label = ctk.CTkLabel(master = frame, text = "Main Menu")
        label.pack(pady = 20)

        button = ctk.CTkButton(master = frame, text = "Resource Tracker", width = 180, height = 32,command = self.trackMenu)
        button.pack(pady = 30)    

        button = ctk.CTkButton(master = frame, text = "Admin Login", width = 180, height = 32, command=None)
        button.pack(pady = 30)

        def logout():
            self.delete('Menu')
            global buttoncount
            global adminvar
            buttoncount = 0 
            adminvar = 0
            self.add_logintab()
        button = ctk.CTkButton(master = frame, text = "Logout", width = 150, height = 30, command = logout)
        button.pack(pady = 25)


    def login(self):
        global buttoncount
        global adminvar
        entered_username = self.user_entry.get().strip()
        entered_password = self.user_pass.get()

        cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ? AND teacher = ?', (entered_username, entered_password,"yes"))
        result = cursor.fetchone()


        if buttoncount <= 0:
            if result:
                tkmb.showinfo(title="Login Approved", message="You have logged in successfully")
                buttoncount = buttoncount + 1
                self.add_menu()
                if result[4] == "yes":
                    adminvar = 1
                else:
                    adminvar = 0
    
            else:
                
                self.perm = ctk.CTkLabel(self.frame, text_color='red',text = 'Invalid Username or Password')
                self.perm.pack()
                self.after(1500,self.perm.destroy)
        else:
            tkmb.showerror(title = "Invalid input",message = "You're already logged in")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title('Inventory Manager')
        self.geometry("600x500")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill ='both', expand = True)
    
        self.container = Main(self.frame)
        self.container.pack(fill ='both', expand = True)
        self.container.add_logintab()

    
app = App()
app.after(0, lambda:app.state("zoomed"))
app.mainloop()