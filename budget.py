import tkinter as tk
from tkinter import messagebox
import sqlite3 as sq

# Database setup
connection = sq.connect('finance_database.db')
connection_cursor = connection.cursor()

# Create the finance table if it doesn't already exist
connection_cursor.execute('''CREATE TABLE IF NOT EXISTS finance (
                                date TEXT,
                                type TEXT,
                                category TEXT,
                                amount REAL
                            )''')

connection.commit()

class TransactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Manager")
        
        # Add labels and entry widgets for transaction details
        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=0, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1)

        self.type_label = tk.Label(root, text="Transaction Type (income/expense):")
        self.type_label.grid(row=1, column=0)
        self.type_entry = tk.Entry(root)
        self.type_entry.grid(row=1, column=1)

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=2, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=2, column=1)

        self.category_label = tk.Label(root, text="Category (optional):")
        self.category_label.grid(row=3, column=0)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=3, column=1)

        # Add buttons for actions
        self.add_button = tk.Button(root, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=4, column=0, columnspan=2)

        self.view_button = tk.Button(root, text="View All Transactions", command=self.view_transactions)
        self.view_button.grid(row=5, column=0, columnspan=2)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=6, column=0, columnspan=2)

    def add_transaction(self):
        """ Adds transaction to the database from the Tkinter form """
        date = self.date_entry.get()
        transaction_type = self.type_entry.get()
        amount = float(self.amount_entry.get())
        category = self.category_entry.get() or None
        
        if not date or not transaction_type or not amount:
            messagebox.showerror("Input Error", "Please fill in all the required fields!")
            return
        
        connection_cursor.execute(
            "INSERT INTO finance (date, type, category, amount) VALUES (?, ?, ?, ?)",
            (date, transaction_type, category, amount)
        )
        connection.commit()
        messagebox.showinfo("Success", "Transaction added successfully.")
        self.clear_entries()

    def view_transactions(self):
        """ Displays all transactions in a popup window """
        all_rows = connection_cursor.execute("SELECT * FROM finance").fetchall()

        if not all_rows:
            messagebox.showinfo("No Records", "No transactions found.")
        else:
            # Create a new window to display the transactions
            transaction_window = tk.Toplevel()
            transaction_window.title("All Transactions")
            
            # Display column headers
            headers = ["Date", "Type", "Category", "Amount"]
            for idx, header in enumerate(headers):
                tk.Label(transaction_window, text=header).grid(row=0, column=idx)

            # Display each row of data
            for row_idx, row in enumerate(all_rows, start=1):
                for col_idx, cell in enumerate(row):
                    tk.Label(transaction_window, text=str(cell)).grid(row=row_idx, column=col_idx)

    def clear_entries(self):
        """ Clears the entry fields after adding a transaction """
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionApp(root)
    root.mainloop()
    
    # Close the database connection when the Tkinter window is closed
    connection.close()
