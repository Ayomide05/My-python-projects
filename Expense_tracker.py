from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from datetime import datetime
from tkinter import filedialog
from tkcalendar import DateEntry

class Expense:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1000x550")
        self.root.configure(bg = "#232323")
        #self.root.resizable(0,0)

        style = ttk.Style()
        style.theme_use("clam")  # "clam" allows more styling options

        style.configure("CustomCombobox.TCombobox",
                fieldbackground="white",  # inside background
                background="white",       # dropdown background
                foreground="black",       # text color
                bordercolor="#000000",
                relief="solid",
                padding=5)
        style.map("CustomCombobox.TCombobox",
          fieldbackground=[('readonly', 'white')],
          background=[('readonly', 'white')],
          foreground=[('readonly', 'black')])
       
        title = Label(self.root, text="Expense Tracker", width=60, font=("ariel", 20, "italic", "bold"), bd=2, bg="#232323", fg="#ffffff")  
        title.pack(pady=10) 

        #---------------- Form frame ----------------
        form_frame = Frame(root, bg="#232323")
        form_frame.pack(fill='x', padx=10, pady=20)
        form_frame.columnconfigure(1, weight=1)

        #Date Entry
        Label(form_frame, text="Date: ", font=("Helvetica", 15, "italic", "bold"), bd=2, bg="#232323", fg="#ffffff")\
        .grid(row=0, column=0, sticky="w", pady=5, padx=(10, 10))
        self.date_entry = DateEntry(form_frame, width=18, bg="white", fg="black", bd=2, font=("Helvetica", 12), date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, sticky="ew", padx=(0,10), pady=5, ipadx=5) 
        #Item Entry
        Label(form_frame, text="Item: ", font=("Helvetica", 15, "italic", "bold"), bd=2, bg="#232323", fg="#ffffff")\
        .grid(row=1, column=0, sticky="w", pady=5, padx=(10, 10))
        self.item_entry = Entry(form_frame, bg="white", fg="black", bd=2, relief="solid", font=("Helvetica", 12))
        self.item_entry.grid(row=1, column=1, sticky="ew", padx=(0,10), pady=5, ipadx=5) 
        #Category Entry
        Label(form_frame, text="Category: ", font=("Helvetica", 15, "italic", "bold"), bd=2, bg="#232323", fg="#ffffff")\
        .grid(row=2, column=0, sticky="w", pady=5, padx=(10, 10))
        category_options = [" ", "Food and Groceries", "Transport", "Clothing", "Skincare", "Utilities & Entertainment","Others"]
        self.category_entry = ttk.Combobox(form_frame, values=category_options, state="readonly", style="CustomCombobox.TCombobox", font=("Helvetica", 12))
        self.category_entry.grid(row=2, column=1, sticky="ew", padx=(0,10), pady=5)
        self.category_entry.current(0)
        #Quantity Entry
        Label(form_frame, text="Quantity: ", font=("Helvetica", 15, "italic", "bold"), bd=2, bg="#232323", fg="#ffffff")\
        .grid(row=3, column=0, sticky="w", pady=5, padx=(10, 10))
        self.quantity_entry = Entry(form_frame, bg="white", fg="black", bd=2, relief="solid", font=("Helvetica", 12))
        self.quantity_entry.grid(row=3, column=1, sticky="ew", padx=(0,10), pady=5, ipadx=5) 
        self.quantity_entry.bind("<KeyRelease>", self.update_amount)
        #Cost_Per_Unit Entry
        Label(form_frame, text="Cost_Per_Unit: ", font=("Helvetica", 15, "italic", "bold"), bd=2, bg="#232323", fg="#ffffff")\
        .grid(row=4, column=0, sticky="w", pady=5, padx=(10, 10))
        self.cpu_entry = Entry(form_frame, bg="white", fg="black", bd=2, relief="solid", font=("Helvetica", 12))
        self.cpu_entry.grid(row=4, column=1, sticky="ew", padx=(0,10), pady=5, ipadx=5) 
        self.cpu_entry.bind("<KeyRelease>", self.update_amount)
        #Amount
        Label(form_frame, text="Amount: ", font=("Helvetica", 15, "italic", "bold"), bd=2, bg="#232323", fg="#ffffff")\
        .grid(row=5, column=0, sticky="w", pady=5, padx=(10, 10))
        self.amount_entry = Entry(form_frame, bg="white", fg="black", bd=2, relief="solid", font=("Helvetica", 12),  state="readonly")
        self.amount_entry.grid(row=5, column=1, sticky="ew", padx=(0,10), pady=5, ipadx=5) 
    
        # Buttons Frame
        button_frame = Frame(self.root, bg="#232323")
        button_frame.pack(pady=20)

        add_btn = Button(button_frame, text="Add Expense", font=("Helvetica", 15, "bold"), bg="green", fg="white", padx=40, pady=5, command=self.add_expense)
        add_btn.grid(row=0, column=0, padx=40)
        
        analyse_btn = Button(button_frame, text="Analyse", font=("Helvetica", 15, "bold"), bg="#007BFF", fg="white", padx=40, pady=5, command=self.analyse_expenses)
        analyse_btn.grid(row=0, column=1, padx=60)

        save_btn = Button(button_frame, text="Save to CSV", font=("Helvetica", 15, "bold"), bg="#FFA500", fg="white", padx=40, pady=5, command=self.save_to_csv)
        save_btn.grid(row=0, column=2, padx=60)

        #--------------------- Create a Table ----------------------------------------
        table_frame = Frame(self.root, bg="#232323")
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Scrollbar for the table
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create Treeview for displaying expenses
        self.expense_table = ttk.Treeview(
            table_frame,
            columns=("Date", "Item", "Category", "Quantity", "Cost", "Amount"),
            show="headings",
            yscrollcommand=scrollbar.set
        )

        # Define table headings
        for col in ("Date", "Item", "Category", "Quantity", "Cost", "Amount"):
            self.expense_table.heading(col, text=col)
            self.expense_table.column(col, anchor="center", width=100)

        self.expense_table.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.expense_table.yview)  

        self.analyse_frame = Frame(self.root, bg="#232323")
        self.analyse_frame.pack(pady=20)

        
    def update_amount(self, event=None):
            try:
                quantity = float(self.quantity_entry.get())
                cost = float(self.cpu_entry.get())
                amount = quantity * cost
                self.amount_entry.configure(state='normal')
                self.amount_entry.delete(0, END)
                self.amount_entry.insert(0, f"{amount:.2f}")
                self.amount_entry.configure(state='readonly')
            except ValueError:
                self.amount_entry.configure(state='normal')
                self.amount_entry.delete(0, END)
                self.amount_entry.insert(0, "")
                self.amount_entry.configure(state='readonly')  
    def clear_form(self):
        self.date_entry.delete(0, END)
        self.item_entry.delete(0, END)
        self.category_entry.current(0)
        self.quantity_entry.delete(0, END)
        self.cpu_entry.delete(0, END)
        self.amount_entry.configure(state='normal')
        self.amount_entry.delete(0, END)
        self.amount_entry.configure(state='readonly')
        
    def add_expense(self):
        date = self.date_entry.get().strip()
        item = self.item_entry.get().strip()
        category = self.category_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        cost = self.cpu_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not date or not item or not category or not quantity or not cost or not amount:
            messagebox.showerror("Missing Information", "Please fill in all fields before adding an expense.")
            return
        print(f"Expense added: Date={date}, Item={item}, Category={category}, Quantity={quantity}, Cost={cost}, Amount={amount}")
        self.expense_table.insert("", "end", values=(date, item, category, quantity, cost, amount))
        self.clear_form() 
        
        
    def analyse_expenses(self):
        top = Toplevel(self.root)
        top.title("Expense Analysis")
        top.geometry("800x600")
        
       
        # Group Data from the Treeview
        expenses = {}
        date_data = {}

        for child in self.expense_table.get_children():
            values = self.expense_table.item(child)['values']
            date, item, category, amount = values[0], values[1], values[2], float(values[5])  # Using Amount

            # Group by category
            expenses[category] = expenses.get(category, 0) + amount
            # Group by date
            date_data[date] = date_data.get(date, 0) + amount

        total_spent = sum(expenses.values())  
        total_label = Label(top, text=f"Total Amount Spent: ₦{total_spent:,.2f}", font=("Arial", 14, "bold"), fg="darkgreen").pack(pady=10)
        
        # --- First Plot: Pie Chart for Category Breakdown ---
        fig1 = plt.Figure(figsize=(4, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%', startangle=140)
        ax1.set_title("Expenses by Category")

        pie_canvas = FigureCanvasTkAgg(fig1, master=top)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        # --- Bar Chart for Expense Over Time ---
        fig2 = plt.Figure(figsize=(4, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        sorted_dates = sorted(date_data.items())
        dates = [d[0] for d in sorted_dates]
        amounts = [d[1] for d in sorted_dates]

        ax2.bar(dates, amounts, color='skyblue')
        ax2.set_title("Expenses Over Time")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Total Spent")
        ax2.tick_params(axis='x', rotation=45)

        bar_canvas = FigureCanvasTkAgg(fig2, master=top)
        bar_canvas.draw()
        bar_canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
    
    def save_to_csv(self):
        if not self.expense_table.get_children():
            messagebox.showwarning("No Data", "There is no data to save.")
            return

        # Prompt user to select file location
        file_path = filedialog.asksaveasfilename(
            defaultextension = ".csv",
            filetypes=[("CSV files","*.csv")],
            initialfile=f"Expenses_{datetime.now().strftime('%Y-%m-%d')}.csv"
        ) 
        if not file_path:
            return
        try:
            with open(file_path, mode="w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                #Write headers
                writer.writerow(["Date", "Item", "Category", "Quantity", "Cost", "Amount"])
                #Write data
                for row_id in self.expense_table.get_children():
                    row = self.expense_table.item(row_id)['values']
                    writer.writerow(row)
            messagebox.showinfo("Success", f"Expenses saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV: {e}")

def main():
    root = Tk()      #Create a special window
    my_exptrk = Expense(root)   # Make a to-do list in that window
    root.mainloop()   # Show the window on the computer screen when you run the program

if __name__ == "__main__":  #This means that when the name that is specified when you want to run the program is the same as the name that this particular file is saved with then it should run the main function
    main()