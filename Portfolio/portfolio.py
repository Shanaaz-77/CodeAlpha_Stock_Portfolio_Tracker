import tkinter as tk
from tkinter import messagebox, filedialog, ttk

# Hardcoded dictionary of stock prices
stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOG": 2700,
    "MSFT": 300
}

portfolio = {}  # Store stock quantities


# Function to add stock
def add_stock():
    stock = stock_var.get()
    qty = quantity_entry.get()

    if not qty.isdigit():
        messagebox.showerror("Error", "Please enter a valid quantity.")
        return

    qty = int(qty)
    portfolio[stock] = portfolio.get(stock, 0) + qty

    quantity_entry.delete(0, tk.END)


# Function to open results page
def open_results():
    if not portfolio:
        messagebox.showerror("Error", "Portfolio is empty. Add some stocks first.")
        return

    results_window = tk.Toplevel(root)
    results_window.title("📊 Portfolio Results")
    results_window.geometry("500x400")
    results_window.configure(bg="#f6e3f2")

    tk.Label(results_window, text="Your Portfolio", font=("Arial", 16, "bold"),
             bg="#f6e3f2", fg="#2c3e50").pack(pady=10)

    # Table for portfolio
    tree = ttk.Treeview(results_window, columns=("Stock", "Quantity", "Price", "Value"), show="headings", height=10)
    tree.heading("Stock", text="Stock")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price ($)")
    tree.heading("Value", text="Value ($)")

    tree.column("Stock", anchor="center")
    tree.column("Quantity", anchor="center")
    tree.column("Price", anchor="center")
    tree.column("Value", anchor="center")

    total_value = 0
    for stock, qty in portfolio.items():
        value = stock_prices[stock] * qty
        total_value += value
        tree.insert("", "end", values=(stock, qty, stock_prices[stock], value))

    tree.pack(pady=10)

    # Total Label
    tk.Label(results_window, text=f"💰 Total Investment Value: ${total_value}",
             font=("Arial", 14, "bold"), fg="green", bg="#f6e3f2").pack(pady=10)

    # Save Button
    tk.Button(results_window, text="Save to File", font=("Arial", 12), bg="#3498db", fg="white",
              command=lambda: save_to_file(total_value)).pack(pady=5)


# Function to save results to file (formatted table)
def save_to_file(total_value):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "w") as file:
            # Header
            file.write("Stock   | Quantity | Price($) | Value($)\n")
            file.write("-" * 42 + "\n")

            # Portfolio rows
            for stock, qty in portfolio.items():
                value = stock_prices[stock] * qty
                file.write(f"{stock:<7} | {qty:<8} | {stock_prices[stock]:<8} | {value:<8}\n")

            # Total
            file.write("-" * 42 + "\n")
            file.write(f"Total Investment Value: ${total_value}\n")

        messagebox.showinfo("Success", f"Portfolio saved to {file_path}")


# ---------------- Main GUI ----------------
root = tk.Tk()
root.title("📈 Stock Portfolio Tracker")
root.geometry("400x300")
root.configure(bg="#f6e3f2")

# Dropdown for stock selection
tk.Label(root, text="Select Stock:", font=("Arial", 12, "bold"), bg="#f6e3f2").pack(pady=5)
stock_var = tk.StringVar(value="AAPL")  # Default value
stock_menu = tk.OptionMenu(root, stock_var, *stock_prices.keys())
stock_menu.config(font=("Arial", 12))
stock_menu.pack()

# Quantity input
tk.Label(root, text="Enter Quantity:", font=("Arial", 12, "bold"), bg="#f894f5").pack(pady=5)
quantity_entry = tk.Entry(root, font=("Arial", 12))
quantity_entry.pack()

# Buttons
tk.Button(root, text="➕ Add Stock", command=add_stock, font=("Arial", 12),
          bg="#27ae60", fg="white").pack(pady=10)
tk.Button(root, text="📊 Show Portfolio", command=open_results, font=("Arial", 12),
          bg="#2980b9", fg="white").pack(pady=5)

root.mainloop()
