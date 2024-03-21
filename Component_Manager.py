import importlib
import subprocess
import sqlite3
db_connection = sqlite3.connect('project.db')
cursor = db_connection.cursor()

import sqlite3

# Connect to the database
db_connection = sqlite3.connect('project.db')
cursor = db_connection.cursor()

# Function to check if inout table is empty
def is_inout_empty():
    cursor.execute('SELECT COUNT(*) FROM inout')
    count = cursor.fetchone()[0]
    return count == 0

# Function to insert values into inout table
def insert_inout_values():
    try:
        cursor.execute('INSERT OR IGNORE INTO inout (incount, outcount) VALUES (?, ?)', (0, 0))
        db_connection.commit()
        print("Values inserted into inout table.")
    except sqlite3.Error as e:
        print("Error inserting values into inout table:", e)







def lib():
    # Define custom library names
    required_libraries = {
        'ctk': 'customtkinter',
        'tkmb': 'tkinter.messagebox',
        'sqlite3': 'sqlite3',
        'yagmail': 'yagmail',
        'CTkTable': 'CTkTable',
        'pillow':'pillow',
        'matplotlib':'matplotlib',
        'hashlib':'hashlib',
        'datetime':'datetime'
        
    }


    #Assigns the first key as variable custom_name
    #Assings the second key as the actual_name
    #Loops through the dictionary required_libraries when it is a tuple in a list
    for custom_name, actual_name in required_libraries.items():
        try:
            #tries to 
            importlib.import_module(actual_name)
            print(f"{custom_name} (as {actual_name}) is already installed.")
        except ImportError:
            print(f"{custom_name} (as {actual_name}) is not installed. Attempting to install...")
            try:
                subprocess.check_call(['pip', 'install', actual_name])
                print(f"{custom_name} (as {actual_name}) has been successfully installed.")
            except subprocess.CalledProcessError:
                print(f"Failed to install {custom_name} (as {actual_name}). Please install it manually.")

lib()   
import customtkinter as ctk
import tkinter.messagebox as tkmb
import CTkTable,yagmail,hashlib
from datetime import *
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

global buttoncount

buttoncount = 0

global adminvar
adminvar = 0
#Database creation


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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS inout (
        incount INTEGER NOT NULL,        
        outcount INTEGER NOT NULL
               
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS setup(
        binary INTEGER PRIMARY KEY NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS log (
        action TEXT NOT NULL,        
        amount INTEGER NOT NULL,
        account TEXT,
        time TEXT,
        item TEXT,
        pk INTEGER PRIMARY KEY NOT NULL
    )
''')



# Check if inout table is empty and insert values if necessary
if is_inout_empty():
    insert_inout_values()

db_connection.commit()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class Main(ctk.CTkTabview):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.name = 'Main'



    def trackMenu(self):
        self.delete(self.name)
        self.name = 'Track'
        self.rtm = self.add(self.name)
        global rsearch
        frame = ctk.CTkScrollableFrame(master = self.rtm)
        frame.pack(pady=100,ipady = 100,ipadx=100, expand=False)

        lable = ctk.CTkLabel(master = frame, text = "Enter reasource name")
        lable.pack()
        self.searchBox = ctk.CTkEntry(master = frame, placeholder_text="Enter Resource name")
        self.searchBox.pack(pady = 30)
        search_button = ctk.CTkButton(master = frame,command=self.search, text="Search")
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


    def search(self):
        if self.searchBox.get() != "":
            if self.searchBox.get().strip().lower() != None:
                rsearch = self.searchBox.get().strip().lower()
            
            cursor.execute('SELECT * FROM resources WHERE rname = ?', (rsearch,))
            self.result = cursor.fetchone()
            if self.result is not None: 
                def showinfo():
                    self.delete(self.name)
                    self.name = "Result"
                    self.resulttab = self.add(self.name)
                    info_font = ctk.CTkFont(family = "Arial", weight = 'bold', size = 23)
                    self.resulttab.grid_columnconfigure(0, weight = 1)
                    self.resulttab.grid_columnconfigure(1, weight = 1)
                    self.resulttab.grid_columnconfigure(2, weight = 1)
                    self.resulttab.grid_rowconfigure(3, weight = 1)   
                             
                    self.resulttab.grid_rowconfigure(0, weight = 1)
                    self.resulttab.grid_rowconfigure(1, weight = 1)
                    self.resulttab.grid_rowconfigure(2, weight = 1)
                    self.resulttab.grid_rowconfigure(3, weight = 1)

                    rname = ctk.CTkLabel(master = self.resulttab,text = self.result[1].upper(), font = info_font)
                    rname.grid(row=0, column=1)

                    frame = ctk.CTkFrame(master = self.resulttab, fg_color= 'white')
                    frame.grid(row=1,column=1,ipady=100, ipadx=100)
                    frame.grid_propagate(False)
                
                    rcount = ctk.CTkLabel(master = frame, text = 'Current count: ' + str(self.result[2]), font = info_font, text_color = 'black') 
                    rcount.pack(pady = 20)                        
                    rmin = ctk.CTkLabel(master = frame, text = 'Minimum count: '+ str(self.result[3]), font = info_font, text_color = 'black')
                    rmin.pack(pady = 20)
                    
                    takeamount = ctk.CTkEntry(master = frame, placeholder_text= 'Enter Amount to take/order')
                    takeamount.pack()
                    
                    self.orderflag = 0
                    
                    def order():
                        if not (takeamount.get() == "" or int(takeamount.get()) <= 0):       
                            if self.orderflag >0:
                                ordertime = (datetime.now(tz=None))
                                order_ammount = takeamount.get()
                                ordertime = str(f"{ordertime.year}/{ordertime.day}/{ordertime.month}/{ordertime.hour}:{ordertime.minute}")
                                inserted_data = (self.result[1],order_ammount, ordertime)
                                insert_sql = "INSERT INTO orders(orname,ocount,otime) VALUES(?,?,?)"
                                cursor.execute(insert_sql, inserted_data)
                                time = (datetime.now(tz=None))
                                time = str(f"{time.day}/{time.month} | {time.hour}:{time.minute}")                                   
                                cursor.execute('INSERT INTO log(action,amount,account,time,item) VALUES(?,?,?,?,?)', ("Order", order_ammount,self.current_log, time,self.result[1]))                                    
                                db_connection.commit()
                                self.orderbutton.destroy()
                                sucess = ctk.CTkLabel(master=frame, text="Successfully sent in order request.")
                                sucess.pack()
                                self.orderflag = 0
                            
                            try:
                                self.orderbutton.configure(text = "Confirm?", fg_color="red")
                                self.orderflag=1
                            except:
                                pass
                        else:
                            tkmb.showerror("Error", "Please enter a valid amount.")



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
                            cursor.execute('SELECT outcount FROM inout')
                            out = cursor.fetchone()
                            outamount = out[0] + take_amount
                            cursor.execute('UPDATE inout SET outcount = ?',(outamount,))
                            time = (datetime.now(tz=None))
                            time = str(f"{time.day}/{time.month} | {time.hour}:{time.minute}")
                            cursor.execute('INSERT INTO log(action,amount,account,time,item) VALUES(?,?,?,?,?)', ("Take", take_amount, self.current_log, time,self.result[1]))
                            db_connection.commit()
                            perm = ctk.CTkLabel(master = frame, text_color='green',text = (f"Amount {str(take_amount)} taken successfully."))
                            perm.pack()
                            self.after(1500,perm.destroy)
                            cursor.execute('SELECT * FROM resources WHERE rname = ?', (rsearch,))
                            self.result = cursor.fetchone()
                            rcount.configure(text = 'Current count: ' + str(self.result[2]))
                            
                            if self.result[2]<= self.result[3] or take_amount>=self.result[2]:
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
                    self.orderbutton.pack()


                    backbutton = ctk.CTkButton(master = self.resulttab, text = "Back", command=self.add_menu)
                    backbutton.grid(row=2,column=1)
                showinfo()
            else:
                noinfo = ctk.CTkLabel(master = self.rtm, text_color='red',text = 'Invalid Input')
                noinfo.pack()
                self.after(1500,noinfo.destroy)



    def adminMenu(self):
        self.delete(self.name)
        self.name = 'Admin'
        self.admintab = self.add(self.name)     
        
        font = ctk.CTkFont(family = "Helvetica", weight = 'bold', size = 23)
        label = ctk.CTkLabel(master = self.admintab, text = "Admin Dashboard",font = font)
        label.grid(row = 0, column = 1) 

        self.admintab.grid_columnconfigure(0, weight = 1)
        self.admintab.grid_columnconfigure(1, weight = 1)
        self.admintab.grid_columnconfigure(2, weight = 1)
        self.admintab.grid_rowconfigure(0, weight = 1)
        self.admintab.grid_rowconfigure(1, weight = 1)
        self.admintab.grid_rowconfigure(2, weight = 1)
        
        center_frame = ctk.CTkFrame(self.admintab, width=500, height= 500)
        center_frame.grid(row = 1,column = 1)
        center_frame.grid_propagate(False)
        
        #in this frame you can add in a log for the people who have logged in and the actions that they have taken.
        left_frame = ctk.CTkScrollableFrame(self.admintab,width=500, height= 500)
        left_frame.grid(row = 1,column = 0)

        right_frame = ctk.CTkFrame(self.admintab,width=500, height= 500)
        right_frame.grid(row = 1,column = 2)


        bottom_frame = ctk.CTkScrollableFrame(self.admintab)
        bottom_frame.grid(row=2, column=0,padx = 65, pady=20, columnspan=3,sticky = "nsew")
        tabview = ctk.CTkTabview(master = bottom_frame)
        tabview.pack()
        orders = tabview.add("Orders")
        current_stored = tabview.add("Current Stored")


        
        cursor.execute('SELECT rname FROM resources')
        result = cursor.fetchall()
        #Fetches all data from the orders table in the database. 
        cursor.execute('SELECT * FROM orders ORDER BY pk DESC')
        orders_result = cursor.fetchall()
        try:
            table = CTkTable.CTkTable(master = current_stored, values = result)
            table.pack()
        except:
            pass
        right_frame.grid_rowconfigure(0, weight = 1)
        right_frame.grid_columnconfigure(0, weight = 1)
        left_frame.grid_rowconfigure(0, weight = 1)
        left_frame.grid_columnconfigure(0, weight = 1)
        
        #chart creation
                
        figure = Figure(figsize=(5, 5), dpi=100)
        subplot = figure.add_subplot(1  , 1, 1)
        categories = ['In', 'Out']
        cursor.execute('SELECT incount,outcount FROM inout')
        count = cursor.fetchone()
        try:
            values = [count[0],count[1]]
            subplot.bar(categories, values)
            subplot.set_title('In and Out')
            subplot.set_xlabel('In/Out')
            subplot.set_ylabel('Amount')
            canvas = FigureCanvasTkAgg(figure, master=right_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row = 0,column=0)
            right_frame.grid_propagate(False)
        #end of chart
        except:
            no_data = ctk.CTkLabel(right_frame, text = "No Data")
            no_data.grid()
            right_frame.grid_propagate(False)

        cursor.execute('SELECT * FROM log ORDER BY pk DESC')
        logs = cursor.fetchall()
        #This tries to add a table with logs on it.
        try:
            logtext = ctk.CTkLabel(master = left_frame, text = "Logs", font = font)
            logtext.grid(row = 0, column= 0, pady = (0,10))
            table = CTkTable.CTkTable(master=left_frame, values = logs)
            table.add_row(values = ["Action","Amount", "User","Time","From","Order"], index = 0)
            table.delete_column(5)
            table.grid(row = 1, column = 0) 
        except:
            pass
        
        #This is the function which will link to a button allowing 
        #For the table's information to be cleared.
        def clear1():
            def clear():
                cursor.execute('DELETE FROM orders WHERE pk <> 0')
                db_connection.commit()
                clearButton.configure(text = "Cleared", fg_color = "red")
                
            clearButton.configure(text  = "Are you sure", command = clear)
        #Will try and create the orders table inside of the tab.
        try:
            otable = CTkTable.CTkTable(master = orders, values = orders_result)
            otable.grid(row =1, column = 2)
            otable.add_row(values = ["OrderID","Resource Name","Order Amount","Time"], index = 0)
            otable.delete_column(0)
            clearButton = ctk.CTkButton(master = orders, text ="Clear",command = clear1)    
            clearButton.grid(row =0,column=2)
        #If it can't it will just  say in the orders tab "No Orders"
        except:
            no_orders = ctk.CTkLabel(orders, text = "No Orders")
            no_orders.pack()
            

        def gobackmenu2():
            self.add_menu()
        goback = ctk.CTkButton(master = self.admintab, text= "Back", command =gobackmenu2, )
        goback.grid(row = 3,column = 1)

        
        def new_re():
            self.delete(self.name)
            self.name = "New Resource"
            self.new = self.add(self.name)
            
            self.new.grid_columnconfigure(0, weight = 1)
            self.new.grid_columnconfigure(1, weight = 1)
            self.new.grid_columnconfigure(2,weight = 1)
            self.new.grid_rowconfigure(0, weight = 1)
            self.new.grid_rowconfigure(1, weight = 1)
            self.new.grid_rowconfigure(2,weight = 1)
            font = ctk.CTkFont(family = "Helvetica", weight = 'bold', size = 23)
            label = ctk.CTkLabel(master = self.new, text = "Add New Resource",font = font)
            label.grid(row = 0, column = 1) 
                        
            frame = ctk.CTkFrame(master = self.new,width=500, height= 650)
            #All frame dimensions 
            frame.grid_columnconfigure(0, weight = 1)
            frame.grid_columnconfigure(1, weight = 1)
            frame.grid_columnconfigure(2, weight = 1)
            frame.grid_rowconfigure(3, weight = 1)   
                     
            frame.grid_rowconfigure(0, weight = 1)
            frame.grid_rowconfigure(1, weight = 1)
            frame.grid_rowconfigure(2, weight = 1)
            frame.grid_rowconfigure(3, weight = 1)
            frame.grid(row = 1,column=1)
            frame.grid_propagate(False)
            font2 = ctk.CTkFont(family = "Helvetica", weight = 'bold', size = 15)
            enter_name = ctk.CTkLabel(frame, text = "Enter Resource Name:", font = font2)            
            enter_name.grid(row = 0, column = 0)
            enter_count = ctk.CTkLabel(frame, text = "Enter Resource Count:", font = font2)            
            enter_count.grid(row = 1, column = 0)
            enter_min = ctk.CTkLabel(frame, text = "Enter Resource Minimum:", font = font2)            
            enter_min.grid(row = 2, column = 0)    
            enter_order = ctk.CTkLabel(frame, text = "Enter Resource Order:", font = font2)            
            enter_order.grid(row = 3, column = 0)         
            rname = ctk.CTkEntry(master = frame,placeholder_text="Enter Resource Name")
            rname.grid(row = 0 ,column = 1)
            rcount = ctk.CTkEntry(master = frame, placeholder_text="Enter Current Count")
            rcount.grid(row = 1,column = 1)
            rorder = ctk.CTkEntry(master = frame, placeholder_text="Enter Minimum Order")
            rorder.grid(row =2,column = 1)
            rmin =ctk.CTkEntry(master = frame, placeholder_text="Enter Minimum Amount")
            rmin.grid(row =3, column=1)              
            def create():
                if rname.get() !="":
                    name = rname.get()
                    name = name.lower()
                    count = rcount.get()
                    min = rmin.get()
                    order = rorder.get()
                    def add2table():
                        try:
                            cursor.execute('INSERT INTO resources (rname,rcount,rmin,rorder) VALUES(?,?,?,?)',(name,count,min,order,))
                            time = (datetime.now(tz=None))
                            time = str(f"{time.day}/{time.month} | {time.hour}:{time.minute}")
                            cursor.execute('INSERT INTO log(action,amount,account,time,item) VALUES(?,?,?,?,?)', ("New Re", count,self.current_log, time,name))
                            db_connection.commit()
                            tkmb.showinfo(title = "New Resource", message = "New Resource Added Successfully")
                            self.adminMenu()
                            
                        except:
                            tkmb.showerror(title = "Resource Already Exist", message="Resource already exist")
                    
                    try:
                        int(count)
                        int(min)
                        int(order)
                        add2table()
                    except:
                        tkmb.showwarning(title = "Int Error",message= "Counts entered aren't Integer")

                
            
            create = ctk.CTkButton(frame, text = "Create", command = create)
            create.grid(row = 4, column =1)
            back = ctk.CTkButton(frame,text="Back",command = self.adminMenu)
            back.grid(row=4,column =0)
        
        
        #just a reused piece of code which has the search functions commands and conditions with some operations flipped
        def add():
            self.delete(self.name)
            self.name = "Add too resource"
            self.newre = self.add(self.name)
            back = ctk.CTkButton(self.newre,text="Back", command =self.adminlaunch)
            back.grid(row = 2,column =1)
            global rsearch
            self.newre.grid_columnconfigure(1,weight = 1)
            self.newre.grid_rowconfigure(0,weight = 1)
            frame = ctk.CTkFrame(master =self.newre, height=500, width=500)
            frame.grid(row = 0,column = 1)
            frame.propagate(False)

            resource_entry = ctk.CTkEntry(master = frame, placeholder_text = "Resource name or ID")
            resource_entry.pack(pady = 30)
            cursor.execute('SELECT rname FROM resources')
            result = cursor.fetchall()
            table = CTkTable.CTkTable(frame, values = result)

            def search():
                if resource_entry.get() != "":
                    rsearch = resource_entry.get().strip()

                    cursor.execute('SELECT * FROM resources WHERE rname = ?', (rsearch,))
                    result = cursor.fetchone()
                    if result is not None:
                        def showinfo():
                            self.delete(self.name)
                            self.name = "Info"
                            self.info = self.add(self.name)
                            info_font = ctk.CTkFont(family = "Arial", weight = 'bold', size = 23)

                            rname = ctk.CTkLabel(master = self.info, text = result[1].upper(), font = info_font)
                            rname.pack(pady = 20)

                            frame = ctk.CTkFrame(master = self.info, fg_color= 'white',height= 500,width=500)
                            frame.pack(pady=30, padx=40)

                        
                            rcount = ctk.CTkLabel(master = frame, text = (f'Current count: {result[2]}'), font = info_font, text_color = 'black') 
                            rcount.pack(pady = 20)

                            rmin = ctk.CTkLabel(master = frame, text = (f'Minimum count: {result[3]}'), font = info_font, text_color = 'black')
                            rmin.pack(pady = 20)
                            
                            addamount = ctk.CTkEntry(master = frame, placeholder_text= 'Enter Amount to add')
                            addamount.pack()


                            def add2():                            
                                add_amount = addamount.get()
                                def makeint():
                                    try:
                                        int(add_amount)
                                        return True
                                    except:
                                        return False
    
                                    
                                if makeint() == True:
                                    add_amount=int(add_amount)
                                    if  add_amount > 0:
                                        newrcount = result[2]+add_amount

                                        cursor.execute('UPDATE resources SET rcount = ? WHERE rname = ?',(newrcount, rsearch))
                                        cursor.execute('SELECT incount FROM inout')
                                        inamount = cursor.fetchone()
                                        plus = inamount[0] + add_amount
                                        cursor.execute('UPDATE inout SET incount = ?',(plus,))
                                        time = (datetime.now(tz=None))
                                        time = str(f"{time.day}/{time.month} | {time.hour}:{time.minute}")
                                        cursor.execute('INSERT INTO log(action,amount,account,time,item) VALUES(?,?,?,?,?)', ("Add", add_amount, self.current_log, time,result[1]))
                                        db_connection.commit()

                                        tkmb.showinfo(title = "Success", message = ("Ammount", str(add_amount), "Has been added sucessfully"))
                                        
                                        cursor.execute('SELECT * FROM resources WHERE rname = ?',(rsearch,))

                                    else:
                                        tkmb.showerror(message = 'Enter a Positive Real value', title = 'Invalid input')

                                else:
                                    tkmb.showerror(message = 'Enter a integer of base 10', title = 'Invalid input')
                            button = ctk.CTkButton(master = frame, text = "Add", command = add2)
                            button.pack(pady = 20)
                            back = ctk.CTkButton(frame,text="Back", command =self.adminlaunch)
                            back.pack(pady = 20)
                        
                            frame.propagate(False)
                        showinfo()
                    else:
                        tkmb.showerror(message = "This item doesnt exist", title = "Missing item")

                else:
                    tkmb.showerror(message = "Please enter a value")

            button = ctk.CTkButton(master = frame, text = "Search", command = search)
            button.pack(pady =20)
            table.pack()
        button = ctk.CTkButton(master = center_frame, text = "Add to Equipment",command = add)
        add_resource_button = ctk.CTkButton(master = center_frame, text = "Add Resource",command = new_re)
        add_account_button = ctk.CTkButton(master = center_frame, text = "Create New Account",command = self.new_ac)
        center_frame.grid_columnconfigure(0, weight = 1)
        center_frame.grid_rowconfigure(0, weight = 1)
        center_frame.grid_rowconfigure(1, weight = 1)
        center_frame.grid_rowconfigure(2, weight = 1)
        button.grid(row = 0, column = 0)
        add_resource_button.grid(row = 1, column = 0)
        add_account_button.grid(row = 2, column = 0)


        
    def adminlaunch(self):
        if adminvar == True:
            self.adminMenu()
        else:
            tkmb.showerror(message = "You don't have admin access.", title = "No Permission")


    
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

        button = ctk.CTkButton(master = frame, text = "Admin Login", width = 180, height = 32, command=self.adminlaunch)
        button.pack(pady = 30)

        def logout():
            self.delete('Menu')
            global buttoncount
            global adminvar
            buttoncount = 0 
            adminvar = False
            self.current_log = None
            self.add_logintab()
        button = ctk.CTkButton(master = frame, text = "Logout", width = 150, height = 30, command = logout)
        button.pack(pady = 25)


    def login(self):
        global buttoncount
        global adminvar
        entered_username = self.user_entry.get().strip()
        entered_password = self.user_pass.get()

        
        #We need to hash the password to increase the security.
        hashed_password = hashlib.sha1(entered_password.encode()).hexdigest()
        cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ? AND teacher = ?', (entered_username, hashed_password,"yes"))
        result = cursor.fetchone()


        if buttoncount <= 0:
            if result:
                tkmb.showinfo(title="Login Approved", message="You have logged in successfully")
                buttoncount = buttoncount + 1
                self.current_log = self.user_entry.get().strip()
                self.add_menu()
                if result[4] == "yes":
                    adminvar = True
                else:
                    adminvar = False
    
            else:
                
                self.perm = ctk.CTkLabel(self.frame, text_color='red',text = 'Invalid Username or Password')
                self.perm.pack()
                self.after(1500,self.perm.destroy)
        else:
            tkmb.showerror(title = "Invalid input",message = "You're already logged in")
    def new_ac(self):
        self.delete(self.name)
        self.name = "New Account"
        self.account = self.add(self.name)
        
        self.account.grid_columnconfigure(0, weight = 1)
        self.account.grid_columnconfigure(1, weight = 1)
        self.account.grid_columnconfigure(2,weight = 1)
        self.account.grid_rowconfigure(0, weight = 1)
        self.account.grid_rowconfigure(1, weight = 1)
        self.account.grid_rowconfigure(2,weight = 1)
        
        font = ctk.CTkFont(family = "Helvetica", weight = 'bold', size = 23)
        label = ctk.CTkLabel(master = self.account, text = "Create New Account",font = font)
        label.grid(row = 0, column = 1) 
                    
        frame = ctk.CTkFrame(master = self.account,width=500, height= 650)
        frame.grid_columnconfigure(0, weight = 1)
        frame.grid_columnconfigure(1, weight = 1)
        frame.grid_columnconfigure(2, weight = 1)
        frame.grid_rowconfigure(3, weight = 1)   
                    
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_rowconfigure(1, weight = 1)
        frame.grid_rowconfigure(2, weight = 1)
        frame.grid_rowconfigure(3, weight = 1)
        frame.grid(row = 1,column=1)
        frame.grid_propagate(False)
        font2 = ctk.CTkFont(family = "Helvetica", weight = 'bold', size = 15)
        enter_name = ctk.CTkLabel(frame, text = """Enter Account Name:
(No spaces)""", font = font2)            
        enter_name.grid(row = 0, column = 0)
        enter_pass = ctk.CTkLabel(frame, text = """Enter Password:
(No spaces)""", font = font2)            
        enter_pass.grid(row = 1, column = 0)   
        conf_pass = ctk.CTkLabel(frame, text = "Confirm Password:", font = font2)            
        conf_pass.grid(row = 2, column = 0)   
        clearance = ctk.CTkLabel(frame, text = "Clearance level Admin?:", font = font2)            
        clearance.grid(row = 3, column = 0)         
        username = ctk.CTkEntry(master = frame,placeholder_text="Enter Username")
        username.grid(row = 0 ,column = 1)
        password = ctk.CTkEntry(master = frame, placeholder_text="Pass Above 5 Char",show = "*")
        password.grid(row = 1,column = 1)
        confpassword = ctk.CTkEntry(master = frame, placeholder_text="Confirm Password",show ="*")
        confpassword.grid(row = 2,column = 1)
        choice = ctk.CTkOptionMenu(master = frame, values=["No", "Yes"])
        choice.grid(row =3,column = 1)
        
        def confirm():
            print(username.get())
            if username.get().strip() =="" or password.get().strip()=="" or confpassword.get().strip()=="":
                tkmb.showerror(message="Fill all fields", title="Missing Fields")
            else:                    
                if len(confpassword.get())>=5:
                    if confpassword.get() == password.get():
                        import random
                        key = ""
                        for i in range(0,6):
                            key = key+str(random.randint(0,9))
                        try:
                            yag = yagmail.SMTP('inventorymanagerbot','feio avya dxhj dcst')

                            to = ['davis.g@stac.southwark.sch.uk','favisboss@gmail.com']
                            subject = 'DO NOT RESPOND'
                            body = (f"Confirmation key: {key}")
                            yag.send(to=to, subject=subject, contents=body)
                            yag.close()
                            check = ctk.CTkInputDialog(text = "If you want to create a new account, please enter the key sent to the first admin's email")
                            attempt = check.get_input()
                            if attempt== key and choice.get() == "Yes":
                                hashedpass = hashlib.sha1(password.get().encode()).hexdigest()
                                cursor.execute('INSERT INTO accounts (username, password, teacher,admin) VALUES(?,?,?,?)',(username.get(),hashedpass,"yes","yes"))
                                time = (datetime.now(tz=None))
                                time = str(f"{time.day}/{time.month} | {time.hour}:{time.minute}")
                                cursor.execute('INSERT INTO log(action,amount,account,time,item) VALUES(?,?,?,?,?)', ("New Ac",0,username.get(), time,"Admin"))
                                db_connection.commit()
                                if adminvar == True:
                                    self.adminMenu()
                                else:
                                    self.delete(self.name)
                                    self.add_logintab()


                            elif attempt==key and choice.get() == "No":
                                hashedpass = hashlib.sha1(password.get().encode()).hexdigest()
                                cursor.execute('INSERT INTO accounts (username, password, teacher,admin) VALUES(?,?,?,?)',(username.get(),hashedpass,"yes","no"))
                                db_connection.commit()
                                if adminvar == True:
                                    self.adminMenu()
                                else:
                                    self.delete(self.name)
                                    self.add_logintab()
                            else:
                                tkmb.showwarning(message = "Key is invalid.", title = "Invalid Input")
                                resend = ctk.CTkButton(self.account, text = "Resend Confirmation Key", command = confirm)
                                resend.grid(row = 4,column = 1)
                        except:
                            tkmb.showwarning(message = "Could not send confirmation key. Please establish connection and try again.", title = "Invalid Connection")            
                    else:
                        tkmb.showerror(title="Passwords don't match", message="Passwords don't match. Try again")
                else:
                    tkmb.showerror(title="Password has to be longer than 5 Character", message="Password has to be longer than 5 Character")
                
                    
                                         
        confirmbut = ctk.CTkButton(frame,text = "Confirm", command= confirm)
        confirmbut.grid(row = 4,column =1)
        def check_admin():
            if adminvar == True:
                back = ctk.CTkButton(frame, command = self.adminMenu, text= "Back")
                back.grid(row = 4, column= 0)   
            else:
                def delete():
                    if adminvar ==True:
                        self.adminMenu()
                    else:
                        self.delete(self.name)
                        self.add_logintab()
                
                back = ctk.CTkButton(frame, command = delete, text= "Back")
                back.grid(row = 4, column= 0)                 
        check_admin()
                        
 
                
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

        self.logbutton = ctk.CTkButton(self.frame, text='Login', command = self.login)
        self.logbutton.pack(pady = 10)
        

        

       
        self.button = ctk.CTkButton(self.e_tab, text = 'Quit', command = quit)
        self.button.pack()

        register = ctk.CTkButton(self.frame,command =self.new_ac, text = "Register", fg_color="purple", hover_color="grey")
        register.pack()

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
app.geometry("800x800")
app.mainloop()
