from tkinter import ttk
import tkinter as tk
import requests


#API
api_key = "your_api_key"
base_url = "http://api.exchangeratesapi.io/v1/latest"
params = {
    "access_key": api_key
}
response = requests.get(base_url, params=params)
data = response.json()
currencies = data.get("rates", {})
currencie_list = []

#this makes currencies list.
for i in currencies:
    currencie_list.append(i)
#............................


#this function is resposible for search bar's for dropboxes.
def search_bar(event, bar):
    value = event.widget.get()

    if value == '':
        bar["values"] = currencie_list
    else:
        data = []
        for item in currencie_list:
            if item.lower().startswith(value.lower()):
                data.append(item)
                
        bar['values'] = data
        
        if data:
            bar.selection_clear()
#...........................................................


# The code which opens the window in the middle of the screen.
root = tk.Tk()
root.title("Currency Exchanger")

window_width = 330
window_height = 290

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
# ........................................................


#Main label with big letters and blu background.
project_title = tk.Label(root, 
                         text="Currency Converter",
                         padx=35, 
                         pady=20, 
                         font=("Arial", 22), 
                         background="midnightblue", 
                         foreground="white")
project_title.pack()

# "from"'s and "to"'s labels
money_from = tk.Label(root, text="FROM:", font=("Arial", 10))
money_from.place(x=20, y=100)

money_to = tk.Label(root, text="TO:", font=("Arial", 10))
money_to.place(x=170, y=100)

amount_label = tk.Label(root, text="AMOUNT:", font=("Arial", 10))
amount_label.place(x=20, y=150)
#............................

# "from"'s, "to"'s and "amount"'s entries
from_entry_dropdown = ttk.Combobox(root, values = currencie_list)
from_entry_dropdown.place(x=20, y=125)
from_entry_dropdown.bind('<KeyRelease>', lambda event: search_bar(event, from_entry_dropdown))

to_entry_dropdown = ttk.Combobox(root, values = currencie_list)
to_entry_dropdown.place(x=170, y=125)
to_entry_dropdown.bind('<KeyRelease>', lambda event: search_bar(event, to_entry_dropdown))

amount_entry = tk.Entry(root, width=48)
amount_entry.place(x=20, y=175)
#......................................

#mathematical Actions and small validations.
def change():
    from_value, to_value, amount_value = get_entries()
    
    # Ensure amount_value is a number
    try:
        amount_value = float(amount_value)
    except ValueError:
        return "Invalid amount"

    # Check if the currencies are valid
    if from_value in currencies and to_value in currencies:
        from_rate = currencies[from_value]
        to_rate = currencies[to_value]
        exchanged_money = (amount_value / from_rate) * to_rate
        return exchanged_money
    else:
        return "Invalid currencies"


#This function gets user's entries.
def get_entries():
    from_value = from_entry_dropdown.get().upper()  
    to_value = to_entry_dropdown.get().upper()      
    amount_value = amount_entry.get()
    return from_value, to_value, amount_value
#...................................


#This function cecks if (from and to) are in the json.
def comparison():
    from_value, to_value, amount_value = get_entries()
    if from_value in currencies and to_value in currencies and amount_value.replace('.', '', 1).isdigit():
        return from_value, to_value, amount_value
    else:
        return "You entered invalid input or invalid amount of money."
#....................................................


#This function prints last result for user. 
def printer():
    answer = change()
    
    if answer != "IDK" and not isinstance(answer, str):  
        from_value, to_value, amount_value = get_entries()
        label = tk.Label(root, text=f"{amount_value} {from_value} = {answer:.2f} {to_value}.")
        label.place(x=20, y=230)
    else:
        label = tk.Label(root, text=answer)
        label.place(x=20, y=230)
#..........................................


# "from"'s, "to"' and "amount"'s button
button = tk.Button(root, 
                   text="CONVERT",
                   padx=15,
                   pady=2,
                   bg="midnightblue",
                   foreground="white",
                   command=printer)  
button.place(x=113, y=200)

root.mainloop()
