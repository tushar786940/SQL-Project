import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create the main application window
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x400")

# Connect to SQLite Database
conn = sqlite3.connect("library.db")
c = conn.cursor()

# Create the books table if it doesn't exist
c.execute("""CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            year INTEGER,
            isbn INTEGER)""")
conn.commit()

# Functions
def add_book():
    c.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)",
              (title_entry.get(), author_entry.get(), year_entry.get(), isbn_entry.get()))
    conn.commit()
    display_books()
    clear_entries()
    messagebox.showinfo("Success", "Book added successfully!")

def delete_book():
    selected_book = book_list.curselection()
    if selected_book:
        book_id = book_list.get(selected_book)[0]
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        display_books()
        messagebox.showinfo("Success", "Book deleted successfully!")
    else:
        messagebox.showwarning("Error", "Please select a book to delete.")

def update_book():
    selected_book = book_list.curselection()
    if selected_book:
        book_id = book_list.get(selected_book)[0]
        c.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
                  (title_entry.get(), author_entry.get(), year_entry.get(), isbn_entry.get(), book_id))
        conn.commit()
        display_books()
        clear_entries()
        messagebox.showinfo("Success", "Book updated successfully!")
    else:
        messagebox.showwarning("Error", "Please select a book to update.")

def display_books():
    book_list.delete(0, tk.END)
    c.execute("SELECT * FROM books")
    for row in c.fetchall():
        book_list.insert(tk.END, row)

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)

def select_book(event):
    selected_book = book_list.curselection()
    if selected_book:
        book = book_list.get(selected_book)
        title_entry.delete(0, tk.END)
        title_entry.insert(tk.END, book[1])
        author_entry.delete(0, tk.END)
        author_entry.insert(tk.END, book[2])
        year_entry.delete(0, tk.END)
        year_entry.insert(tk.END, book[3])
        isbn_entry.delete(0, tk.END)
        isbn_entry.insert(tk.END, book[4])

# UI Components
# Labels
tk.Label(root, text="Title").grid(row=0, column=0)
tk.Label(root, text="Author").grid(row=1, column=0)
tk.Label(root, text="Year").grid(row=2, column=0)
tk.Label(root, text="ISBN").grid(row=3, column=0)

# Entry widgets
title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1)

author_entry = tk.Entry(root)
author_entry.grid(row=1, column=1)

year_entry = tk.Entry(root)
year_entry.grid(row=2, column=1)

isbn_entry = tk.Entry(root)
isbn_entry.grid(row=3, column=1)

# Listbox and scrollbar for displaying books
book_list = tk.Listbox(root, height=10, width=40)
book_list.grid(row=0, column=2, rowspan=6, columnspan=2)
book_list.bind("<<ListboxSelect>>", select_book)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=0, column=4, rowspan=6)

book_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=book_list.yview)

# Buttons
add_button = tk.Button(root, text="Add Book", command=add_book)
add_button.grid(row=4, column=0)

delete_button = tk.Button(root, text="Delete Book", command=delete_book)
delete_button.grid(row=4, column=1)

update_button = tk.Button(root, text="Update Book", command=update_book)
update_button.grid(row=5, column=0)

view_button = tk.Button(root, text="View All Books", command=display_books)
view_button.grid(row=5, column=1)

clear_button = tk.Button(root, text="Clear Fields", command=clear_entries)
clear_button.grid(row=6, column=0, columnspan=2)

# Display initial book list
display_books()

# Run the application
root.mainloop()

# Close the database connection when the application is closed
conn.close()