import sqlite3 as sq
from tkinter import *

# Create database for shop
db = sq.connect("db_shop.db")
cur = db.cursor()
cur.execute("""
            CREATE TABLE IF NOT EXISTS db_shop(
            id INTEGER PRIMARY KEY,
            product TEXT,
            sell TEXT,
            buy INTEGER,
            Num INTEGER)
""")
db.commit()
db.close()

# Add product function
def insert(product, sell, buy, Num):
    db = sq.connect("db_shop.db")
    cur = db.cursor()
    cur.execute('INSERT INTO db_shop(product, sell, buy, Num) VALUES(?, ?, ?, ?)', 
                (product, sell, buy, Num))
    db.commit()
    db.close()

# Delete product function
def delete(product_id):
    db = sq.connect("db_shop.db")
    cur = db.cursor()
    cur.execute("DELETE FROM db_shop WHERE id = ?", (product_id,))
    db.commit()
    db.close()
    

# product search function
def search(product_name):
    db = sq.connect("db_shop.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM db_shop WHERE product = ?", (product_name,))
    rows = cur.fetchall()
    db.close()
    return rows

# View function
def view():
    db = sq.connect("db_shop.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM db_shop")
    rows = cur.fetchall()
    db.close()
    return rows

#Functions  tk
def insert_item():
    product = entry_name.get()
    sell = entry_sell.get()
    buy = entry_buy.get()
    Num = entry_num.get()
    insert(product, sell, buy, Num)
    listbox.delete(0, END)
    listbox.insert(END, (product, sell, buy, Num))

def delete_item():
    selected_item = listbox.curselection()
    if selected_item:
        product_id = listbox.get(selected_item)[0] 
        delete(product_id)
        listbox.delete(selected_item) 
    
def search_product():
    product_name = entry_name.get()
    rows = search(product_name) 
    
    listbox.delete(0, END)
    for row in rows:
        listbox.insert(END, row)

def load_item():
    selected_item = listbox.curselection()
    if selected_item:
        item = listbox.get(selected_item)
        entry_name.delete(0, END)
        entry_name.insert(0, item[1])
        entry_sell.delete(0, END)
        entry_sell.insert(0, item[2])
        entry_buy.delete(0, END)
        entry_buy.insert(0, item[3])
        entry_num.delete(0, END)
        entry_num.insert(0, item[4])
        edit_product.item_id = item[0]


def edit_item():
    product = entry_name.get()
    sell = entry_sell.get()
    buy = entry_buy.get()
    Num = entry_num.get()
    db = sq.connect("db_shop.db")
    cur = db.cursor()
    cur.execute("UPDATE db_shop SET product=?, sell=?, buy=?, Num=? WHERE id=?", 
                (product, sell, buy, Num, edit_product.item_id))
    db.commit()
    db.close()
    refresh_listbox()


def refresh_listbox():
    listbox.delete(0, END)
    for row in view():
        listbox.insert(END, row)


# UI
win = Tk()
win.title("supermarket")
win.geometry("465x250")
# Buttons
add_product = Button(text="add", width=15, height=2, command=insert_item)
add_product.grid(row=3, column=4)
search_product = Button(text="search product", width=15, height=2, command=search_product)
search_product.grid(row=4, column=4)
delete_product = Button(text="delete product", width=15, height=2, command=delete_item)
delete_product.grid(row=5, column=4)
edit_product = Button(text="edit", width=15, height=2, command=edit_item) 
edit_product.grid(row=6, column=4)
close_app = Button(text="close", width=15, height=2, command=win.quit)
close_app.grid(row=7, column=4)
#input & Label
Label_name = Label(text = "name product :")
Label_name.grid(row=0, column=0)
entry_name= Entry(width=20)
entry_name.grid(row=0, column=1)

Label_sell = Label(text = "price sell:")
Label_sell.grid(row=1, column=0)
entry_sell= Entry(width=20)
entry_sell.grid(row=1, column=1)

Label_buy = Label(text = "price buy:")
Label_buy.grid(row=0, column=3)
entry_buy= Entry(width=20)
entry_buy.grid(row=0, column=4)

Label_num = Label(text = "number:")
Label_num.grid(row=1, column=3)
entry_num = Entry()
entry_num.grid(row=1, column=4)

#list & scrol
listbox = Listbox(win,width= 45 , height=9) 
listbox.grid(row=4,column=0, rowspan=4,columnspan=3)
scrollbar = Scrollbar(win)
scrollbar.grid(row=4, column=3, rowspan=6)
listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)
listbox.bind("<<ListboxSelect>>", lambda event: load_item())

refresh_listbox()
win.mainloop()
