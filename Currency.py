import tkinter as tk
from tkinter import messagebox
import requests

class CurrencyConverter:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']
        
    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        converted_amount = round(amount * self.currencies[to_currency], 4)
        return converted_amount

def perform_conversion():
    from_curr = from_currency_var.get()
    to_curr = to_currency_var.get()
    amount_str = amount_entry.get()
    if not amount_str:
        messagebox.showerror("Input error", "Please enter the amount to convert")
        return
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Input error", "Please enter a valid number for amount")
        return

    if from_curr == to_curr:
        messagebox.showinfo("Result", f"{amount} {from_curr} = {amount} {to_curr}")
        return

    try:
        converted = converter.convert(from_curr, to_curr, amount)
        result_var.set(f"{amount} {from_curr} = {converted} {to_curr}")
    except KeyError:
        messagebox.showerror("Currency error", "Selected currency is not supported by the API.")

# URL for real-time exchange rates with USD as base currency (free tier)
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
converter = CurrencyConverter(API_URL)

# Setup Tkinter GUI window
root = tk.Tk()
root.title("Currency Converter")

# Available currencies from the API rates keys
currency_options = list(converter.currencies.keys())
currency_options.sort()

# Variables linked to GUI components
from_currency_var = tk.StringVar(root)
to_currency_var = tk.StringVar(root)
result_var = tk.StringVar(root)

# Default selections
from_currency_var.set("USD")
to_currency_var.set("EUR")

# GUI Layout
tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="From Currency:").grid(row=1, column=0, padx=10, pady=10)
from_currency_menu = tk.OptionMenu(root, from_currency_var, *currency_options)
from_currency_menu.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="To Currency:").grid(row=2, column=0, padx=10, pady=10)
to_currency_menu = tk.OptionMenu(root, to_currency_var, *currency_options)
to_currency_menu.grid(row=2, column=1, padx=10, pady=10)

convert_button = tk.Button(root, text="Convert", command=perform_conversion)
convert_button.grid(row=3, column=0, columnspan=2, pady=20)

result_label = tk.Label(root, textvariable=result_var, font=("Helvetica", 14))
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
