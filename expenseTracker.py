import tkinter as tk
from tkinter import Toplevel, ttk
import sqlite3
from ttkthemes import ThemedStyle
import tkinter.ttk as ttk 
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
import matplotlib.pyplot as plt

class ExpenseTracker:
    # Init function
    def __init__(self, master):
        mainFrame = tk.Frame(master)
        mainFrame.pack()

        self.createNotebook()
        self.addFrame()
        self.viewFrame()
        self.reportFrame()


    def createNotebook(self):
        # Initializing the notebook
        self.myStyle = ttk.Style()
        self.myStyle.configure("TNotebook.Tab", font=("Ariel","12", "bold"))

        self.myNotebook = ttk.Notebook()

        # Frames for each notebook tab
        self.frame1 = tk.Frame(self.myNotebook, width=1700, height=950)
        self.frame1.pack(fill="both", expand=True)
        self.frame2 = tk.Frame(self.myNotebook, width=1700, height=950)
        self.frame2.pack(fill="both", expand=True)
        self.frame3 = tk.Frame(self.myNotebook, width=1700, height=950)
        self.frame3.pack(fill="both", expand=True)

        # Add to our notebook
        self.myNotebook.add(self.frame1, text="Add Expenses")
        self.myNotebook.add(self.frame2, text="View Expenses")
        self.myNotebook.add(self.frame3, text="Report")

        self.myNotebook.pack(pady=15)

    def addFrame(self):
        # Function to add records to database
        def addExpense():
            # Create or connect to a database=
            conn = sqlite3.connect('expenseTracker.db')

            # Create a cursor
            cursor = conn.cursor()

            try:
                date = self.date.get()
                dateObj = datetime.strptime(date, '%m/%d/%Y')
                formatted = dateObj.strftime('%m/%d/%Y')
                #print(date, dateObj)
                # Insert into table
                cursor.execute("INSERT INTO expenseTracker VALUES (:expenseName, :amount, :date, :category, :paymentType)", 
                            {
                                'expenseName': self.expenseName.get(),
                                'amount': self.amount.get(),
                                'date': formatted,
                                'category': categories.get(),
                                'paymentType': pTypes.get(),
                            }
                )

                self.expenseName.delete(0, 'end')
                self.amount.delete(0, 'end')
                self.date.delete(0, 'end')
                categories.set("Choose a Category")
                pTypes.set("Choose a Payment Type")

                # Commit changes
                conn.commit()

                # Close  connection
                conn.close()
                self.frame2.after(1)
            except ValueError:
                self.wrongFormat = messagebox.showerror(title="Error", message="Wrong Date Format")
                tk.Label(self.frame1, text=self.wrongFormat)



        # Option for categories and payment types
        categoriesOptions = [
            "Entertainment",
            "Groceries",
            "Transportation",
            "Food/Eating Out",
            "Clothes",
            "Bills",
            "Education",
            'Other'
        ]

        paymentTypeOptions = [
            "Credit",
            "Debit",
            "Cash",
            "Other"
        ]

        # Variable for category and payment type and amount
        categories = tk.StringVar()
        categories.set(categoriesOptions[0])

        pTypes = tk.StringVar()
        pTypes.set(paymentTypeOptions[0])

        # Creating the labels for the entries
        self.expenseNameLabel = tk.Label(self.frame1, text="Expense Name: ", pady=20, padx=20, font=("Ariel", 15))
        self.amountLabel = tk.Label(self.frame1, text="Amount: $", pady=20, padx=20, font=("Ariel", 15))
        self.dateLabel = tk.Label(self.frame1, text="Date (mm/dd/yyyy): ", pady=20, padx=20, font=("Ariel", 15))
        self.categoryLabel = tk.Label(self.frame1, text="Category: ", pady=20, padx=20, font=("Ariel", 15))
        self.paymentTypeLabel = tk.Label(self.frame1, text="Payment Type: ", pady=20, padx=20, font=("Ariel", 15))

        # Packing labels
        self.expenseNameLabel.grid(row=0, column=0, pady=(50, 0))
        self.amountLabel.grid(row=0, column=2, pady=(50, 0))
        self.dateLabel.grid(row=1, column=0)
        self.categoryLabel.grid(row=1, column=2)
        self.paymentTypeLabel.grid(row=2, column=0)

        # Creating the entries 
        self.expenseName = ttk.Entry(self.frame1, width=40, font=("Ariel", 15))
        self.amount = ttk.Entry(self.frame1, width=40, font=("Ariel", 15))
        #self.amount.insert(0, "$")
        self.date = ttk.Entry(self.frame1, width=40, font=("Ariel", 15))
        self.category = ttk.OptionMenu(self.frame1, categories, categoriesOptions[0], *categoriesOptions)
        self.paymentType = ttk.OptionMenu(self.frame1, pTypes, paymentTypeOptions[0], *paymentTypeOptions)

        # Setting width of dropdown box
        self.category.config(width=59)
        self.paymentType.config(width=59)

        # Packing entries
        self.expenseName.grid(row=0, column=1, pady=(50, 0))
        self.amount.grid(row=0, column=3, pady=(50, 0))
        self.date.grid(row=1, column=1)
        self.category.grid(row=1, column=3)
        self.paymentType.grid(row=2, column=1)

        # Add Expense to Database button
        self.addExpenseButton = ttk.Button(self.frame1, text="Add Expense", command=addExpense)
        self.addExpenseButton.grid(row=6, column=3, pady=100, padx=20, sticky="E")
        

        
    def viewFrame(self):
        def myTreeView(var):
            if var == "delete":
                self.set.destroy()
                self.sb.destroy()
            else:
                # Create or connect to a database
                conn = sqlite3.connect('expenseTracker.db')

                # Create a cursor
                cursor = conn.cursor()

                # Query the database
                cursor.execute("SELECT *, oid FROM expenseTracker ORDER BY date DESC")
                records = cursor.fetchall()

                self.set = ttk.Treeview(self.frame2, height=25)
                #self.set.pack(side='left', anchor='nw')
                self.set.grid(row=0, column=0)

                self.sb = ttk.Scrollbar(self.frame2, orient='vertical')
                #self.sb.pack(side='right', fill='y', pady=(0,390))
                self.sb.grid(row=0, column=1, ipady=253)

                self.set.config(yscrollcommand=self.sb.set)
                self.sb.config(command=self.set.yview)

                self.set['columns']=('id', 'expenseName','amount', 'date', 'category', 'paymentType')
                self.set.column("#0", width=0, stretch='no')
                self.set.column("id", anchor='center', width=100)
                self.set.column("expenseName",anchor='center', width=300)
                self.set.column("amount",anchor='center', width=300)
                self.set.column("date",anchor='center', width=300)
                self.set.column("category",anchor='center', width=350)
                self.set.column("paymentType",anchor='center', width=350)

                self.set.heading("#0",text="",anchor='center')
                self.set.heading("id",text="ID",anchor='center')
                self.set.heading("expenseName",text="Expense Name",anchor='center')
                self.set.heading("amount",text="Amount",anchor='center')
                self.set.heading("date",text="Date",anchor='center')
                self.set.heading("category",text="Category",anchor='center')
                self.set.heading("paymentType",text="Payment Type",anchor='center')

                count = 0
                for rec in records:
                    date = rec[2]
                    dateObj = datetime.strptime(date, '%m/%d/%Y')
                    formattedDate = dateObj.strftime('%A %b %d, %Y')
                    self.set.insert(parent='',index='end', iid=count, text='', values=(str(rec[5]), str(rec[0]), str(rec[1]), formattedDate, str(rec[3]), str(rec[4])))
                    count += 1
                
                # Commit changes
                conn.commit()

                # Close  connection
                conn.close()
            
        myTreeView("create")

        
        def doubleClick(event):
            global rowID
            # Create or connect to a database
            conn = sqlite3.connect('expenseTracker.db')

            # Create a cursor
            cursor = conn.cursor()
            self.editor = tk.Toplevel()
            self.editor.title("Editor")

            rowData = self.set.item(self.set.focus())
            rowID = rowData['values'][0]
            #print(rowID)

            cursor.execute("SELECT * FROM expenseTracker WHERE oid=" + str(rowID))
            records = cursor.fetchall()

            # Option for categories and payment types
            categoriesOptions = [
                "Entertainment",
                "Groceries",
                "Transportation",
                "Food/Eating Out",
                "Clothes",
                "Bills",
                "Education",
                'Other'
            ]

            paymentTypeOptions = [
                "Credit",
                "Debit",
                "Cash",
                "Other"
            ]

            # Variable for category and payment type and amount
            categories = tk.StringVar()

            pTypes = tk.StringVar()

            # Creating the labels for the entries
            self.expenseNameLabelE = tk.Label(self.editor, text="Expense Name: ", pady=20, padx=20, font=("Ariel", 15))
            self.amountLabelE = tk.Label(self.editor, text="Amount: $", pady=20, padx=20, font=("Ariel", 15))
            self.dateLabelE = tk.Label(self.editor, text="Date (mm/dd/yyyy): ", pady=20, padx=20, font=("Ariel", 15))
            self.categoryLabelE = tk.Label(self.editor, text="Category: ", pady=20, padx=20, font=("Ariel", 15))
            self.paymentTypeLabelE = tk.Label(self.editor, text="Payment Type: ", pady=20, padx=20, font=("Ariel", 15))

            # Gridding labels
            self.expenseNameLabelE.grid(row=0, column=0)
            self.amountLabelE.grid(row=0, column=2)
            self.dateLabelE.grid(row=1, column=0)
            self.categoryLabelE.grid(row=1, column=2)
            self.paymentTypeLabelE.grid(row=2, column=0)

            # Creating the entries 
            self.expenseNameE = ttk.Entry(self.editor, width=40, font=("Ariel", 15))
            self.amountE = ttk.Entry(self.editor, width=40, font=("Ariel", 15))
            self.dateE = ttk.Entry(self.editor, width=40, font=("Ariel", 15))
            self.categoryE = ttk.OptionMenu(self.editor, categories, categoriesOptions[0], *categoriesOptions)
            self.paymentTypeE = ttk.OptionMenu(self.editor, pTypes, paymentTypeOptions[0], *paymentTypeOptions)

            # Setting width of dropdown box
            self.categoryE.config(width=59)
            self.paymentTypeE.config(width=59)

            # Packing entries
            self.expenseNameE.grid(row=0, column=1)
            self.amountE.grid(row=0, column=3, padx=(0, 20))
            self.dateE.grid(row=1, column=1)
            self.categoryE.grid(row=1, column=3, padx=(0, 20))
            self.paymentTypeE.grid(row=2, column=1)

            for rec in records:
                self.expenseNameE.insert(0, rec[0])
                self.amountE.insert(1, rec[1])
                self.dateE.insert(0, rec[2])
                categories.set(rec[3])
                pTypes.set(rec[4])
            
            
            # Commit changes
            conn.commit()

            # Close  connection
            conn.close()

            def update():
                global rowID
                # Create or connect to a database=
                conn = sqlite3.connect('expenseTracker.db')

                # Create a cursor
                cursor = conn.cursor()

                try:
                    date = self.dateE.get()

                    # Insert into table
                    cursor.execute("""UPDATE expenseTracker SET 
                        expenseName = :expenseName,
                        amount = :amount,
                        date = :date,
                        category = :category,
                        paymentType = :paymentType

                        WHERE oid= :oid""",
                        {
                            'expenseName': self.expenseNameE.get(),
                            'amount': self.amountE.get(),
                            'date': date,
                            'category': categories.get(),
                            'paymentType': pTypes.get(),

                            'oid': rowID
                        })

                    # Commit changes
                    conn.commit()

                    # Close  connection
                    conn.close()
                    myTreeView("delete")
                    myTreeView("create")
                    self.editor.destroy()
                    self.set.bind("<Double-1>", doubleClick)
                except ValueError:
                    self.wrongFormat = messagebox.showerror(title="Error", message="Wrong Date Format")
                    tk.Label(text=self.wrongFormat)
                    self.editor.lift()
                    self.set.bind("<Double-1>", doubleClick)

            
            def deleteOne():
                # Create or connect to a database=
                conn = sqlite3.connect('expenseTracker.db')

                # Create a cursor
                cursor = conn.cursor()
                
                rowData = self.set.item(self.set.focus())
                rowID = rowData['values'][0]

                # Delete a record
                cursor.execute("DELETE FROM expenseTracker WHERE oid=" + str(rowID))
                # Commit changes
                conn.commit()
                # Close  connection
                conn.close()
                myTreeView("delete")
                myTreeView("create")
                self.editor.destroy()
                self.set.bind("<Double-1>", doubleClick)

            self.delete = ttk.Button(self.editor, text="Delete", command=deleteOne)
            self.delete.grid(row=6, column=3, pady=(100, 25), padx=(20, 240), sticky='E')

            self.cancel = ttk.Button(self.editor, text="Cancel", command=self.editor.destroy)
            self.cancel.grid(row=6, column=3, pady=(100, 25), padx=(20, 135), sticky='E')

            self.save = ttk.Button(self.editor, text="Save Changes", command=update)
            self.save.grid(row=6, column=3, pady=(100, 25), padx=20, sticky="E")
        
        
        directions = 'Double Click To Edit'
        self.informationOnTable = tk.Label(self.frame2, text=directions, bd=1, relief='sunken', anchor='w')
        self.informationOnTable.grid(row=1, column=0, sticky='we')

        def refreshButton():
            myTreeView("delete")
            myTreeView("create")
            self.set.bind("<Double-1>", doubleClick)

        self.refreshButton = ttk.Button(self.frame2, text="Refresh Table", command=refreshButton)
        self.refreshButton.grid(row=2, column=0, pady=10)


        '''
        self.deleteMultiple = ttk.Button(self.frame2, text="Delete Multiple Rows", command=deleteMultiple)
        self.deleteMultiple.grid(row=2, column=0, sticky='w', padx=(200, 10), pady=(40, 0))
        '''
        self.set.bind("<Double-1>", doubleClick)
            
    def reportFrame(self):
        def categorySummary():
            # Create or connect to a database=
            conn = sqlite3.connect('expenseTracker.db')
            # Create a cursor
            cursor = conn.cursor()

            cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE '%Entertainment%' """)
            eTotal = cursor.fetchone()[0]

            cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE '%Groceries%' """)
            gTotal = cursor.fetchone()[0]

            cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE '%Transportation%' """)
            tTotal = cursor.fetchone()[0]

            cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE 'Food/Eating Out%' """)
            fTotal = cursor.fetchone()[0]

            cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE '%Clothes%' """)
            cTotal = cursor.fetchone()[0]

            cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE '%Bills%' """)
            bTotal = cursor.fetchone()[0]

            cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE '%Education%' """)
            edTotal = cursor.fetchone()[0]

            cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE '%Other%' """)
            oTotal = cursor.fetchone()[0]

            allTotals = []
            labels = [
                "Entertainment",
                "Groceries",
                "Transportation",
                "Food/Eating Out",
                "Clothes",
                "Bills",
                "Education",
                'Other'
            ]
            
            allTotals = [eTotal, gTotal, tTotal, fTotal, cTotal, bTotal, edTotal, oTotal]
            for i in range(len(allTotals)):
                if allTotals[i] is None:
                    allTotals[i] = 0
            
            sizes = allTotals
            #explode = (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)

            categorySubplot = plt.subplot()
        
            categorySubplot.pie(sizes, shadow=True, radius=10, startangle=180)
            categorySubplot.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            plt.legend(title="Breakdown:", labels=labels, loc=(-0.15,.65))
            plt.show()
            conn.commit()
            # Close  connection
            conn.close()

        def barSummary():
            labels = [
                "Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"
            ]
            '''
            - grab the sum of each column where month is ex. Jan, and in this current year
            - fetch this data and store it as a variable
            - add this variable to the values list
            '''
            # Create or connect to a database=
            conn = sqlite3.connect('expenseTracker.db')
            # Create a cursor
            cursor = conn.cursor()
            
            currentYear = datetime.now().year
            
            values =  []
            for i in range(1,10):
                cursor.execute(""" select sum(amount) from expenseTracker where date like ? or date like ? and date like ?""", ['0'+str(i)+'%', str(i)+'%', '%' + str(currentYear)])
                monthlyTotals = cursor.fetchall()[0][0]
                if monthlyTotals is None:
                    monthlyTotals = 0
                values.append(monthlyTotals)
            
            for i in range(10,13):
                cursor.execute(""" select sum(amount) from expenseTracker where date like ? and date like ?""", [str(i)+'%', '%' + str(currentYear)])
                monthlyTotals = cursor.fetchall()[0][0]
                if monthlyTotals is None:
                    monthlyTotals = 0
                values.append(monthlyTotals)
                        
            barPlot = plt.figure(figsize = (10, 5))
            
            # creating the bar plot
            plt.bar(labels, values, color ='#ADD8E6',
                    width = 0.4)
            
            plt.xlabel("Month")
            plt.ylabel("Total Spent $")
            plt.title("Monthly Spending  " + "(" + str(currentYear) + ")")
            plt.show()

            conn.commit()
            conn.close()
        
        # Left Side
        self.showCategorySummary = ttk.Button(self.frame3, text="Pie Chart Report", command=categorySummary)
        self.showCategorySummary.grid(row=1, column=0, pady=10, padx=10)

        self.description1 = tk.Label(self.frame3, text="Button generates a report in the form of a pie chart:", font=(15))
        self.description1.grid(row=0, column=0, pady=10, padx=10)

        self.l = tk.Label(self.frame3, text="Example Report:").grid(row=2, column=0, pady=10, padx=10)
        
        self.exPieChart = ImageTk.PhotoImage(Image.open('pictures/exPieChart.png'))
        self.exPieChartlabel = tk.Label(self.frame3, image=self.exPieChart)
        self.exPieChartlabel.grid(row=3, column=0, pady=10, padx=20)

        # Right Side 
        self.showCategorySummary = ttk.Button(self.frame3, text="Bar Chart Report", command=barSummary)
        self.showCategorySummary.grid(row=1, column=1, pady=10, padx=(120, 10))

        self.description1 = tk.Label(self.frame3, text="Button generates a report in the form of a bar chart:", font=(15))
        self.description1.grid(row=0, column=1, pady=10, padx=(120, 10))

        self.l = tk.Label(self.frame3, text="Example Report:").grid(row=2, column=1, pady=10, padx=(120, 10))
    
        self.barChart = ImageTk.PhotoImage(Image.open('pictures/exBarChart.png'))
        self.barChartLabel = tk.Label(self.frame3, image=self.barChart)
        self.barChartLabel.grid(row=3, column=1, pady=10, padx=(80, 20))
    
        



# Creating root window and its settings
root = tk.Tk()
root.title("Expense Tracker")
root.iconbitmap("favicon.ico")
root.state('zoomed')
#root.resizable(False, False)
style = ThemedStyle()
#style.theme_use('plastik')
#style.theme_use('yaru')
style.theme_use('breeze')

# Initializing ExpenseTracker class
obj = ExpenseTracker(root)

root.mainloop()