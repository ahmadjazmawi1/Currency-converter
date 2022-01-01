import requests

from tkinter import *
import tkinter as tk
from tkinter import ttk
import re



class currencyConverter():
    def __init__(self,url):
        #loads the page and converts its contents to json
        self.data = requests.get(url).json()
        self.currency = self.data['rates']
    def convert(self,amount, fromCurrency, to):
        initial = amount
        if fromCurrency !='CAD':
            amount = amount/self.currency[fromCurrency]
        amount = round(amount * self.currency[to], 4)
        return amount

class UI(tk.Tk):
    def __init__(self, converter):
        window = tk.Tk()
        tk.Tk.__init__(self)
        self.title = 'currency Converter'
        self.converter = converter
        self.geometry("500x200")
        self.intro = Label(self, text = "Welcome to my currency converter", fg="blue", relief = GROOVE, borderwidth = 3)
        self.intro.config(font = ('Courier', 15, 'bold'))

        self.intro.place(x=10, y=5)

        '''Text box'''
        valid = self.register(self.validate)
        #self.config(validate="key", validatecommand=(valid, '%P'))
        
        self.amount_field = Entry(self,bd = 3, relief = tk.RIDGE, justify = tk.CENTER,validate='key')
        self.amount_field.config(validate="key", validatecommand=(valid, '%P'))
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 17, borderwidth = 3)

        self.amount_field.place(x = 36, y = 150)
        print(self.amount_field)

        #Dropdown menu
        self.from_var = StringVar(self)
        self.from_var.set("JOD")

        self.to_var = StringVar(self)
        self.to_var.set("CAD")
        f = ("Arial", 12, "bold")
        
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_var,values=list(self.converter.currency.keys()), font = f, state = 'readonly', width = 12, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_var,values=list(self.converter.currency.keys()), font = f, state = 'readonly', width = 12, justify = tk.CENTER)

        # placing
        self.from_currency_dropdown.place(x = 30, y= 120)
        self.amount_field.place(x = 36, y = 150)
        self.to_currency_dropdown.place(x = 340, y= 120)
        
        self.converted_amount_field_label.place(x = 346, y = 150)
        
        # Convert button
        self.convert_button = Button(self, text = "Convert", fg = "black", command = self.perform) 
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x = 225, y = 135)
    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_var.get()
        to_curr = self.to_var.get()

        converted_amount = self.converter.convert(amount,from_curr,to_curr)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text = str(converted_amount))
    def validate(self, string):
        reg = re.compile("[0-9]")
        result = reg.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))


if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/CAD'
    converter = currencyConverter(url)

    UI(converter)
    mainloop()




