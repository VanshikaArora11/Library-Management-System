import tkinter as tk
from tkinter import messagebox
import datetime

class LibraryItem:
    def __init__(self, name, creator, isbn_code):
        self.name = name
        self.creator = creator
        self.isbn_code = isbn_code
        self.is_borrowed = False
        self.due_date = None

    def borrow_item(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            self.due_date = datetime.datetime.now() + datetime.timedelta(days=14)
            return True
        return False

    def return_item(self):
        self.is_borrowed = False
        self.due_date = None

    def __str__(self):
        status = "Available" if not self.is_borrowed else "Borrowed"
        return f"Name: {self.name}, Creator: {self.creator}, ISBN: {self.isbn_code}, Status: {status}, Due Date: {self.due_date.strftime('%Y-%m-%d') if self.due_date else 'N/A'}"


class LibrarySystem:
    def __init__(self):
        self.items = []
        self.users_data = {"admin": "vanshika@123"}

    def add_item(self, name, creator, isbn_code):
        new_item = LibraryItem(name, creator, isbn_code)
        self.items.append(new_item)
        return f"'{name}' by {creator} has been successfully added."

    def borrow_item(self, isbn_code, username):
        if username not in self.users_data:
            return "Invalid username. Please log in first."

        for item in self.items:
            if item.isbn_code == isbn_code:
                if item.borrow_item():
                    return f"You have successfully borrowed '{item.name}'. Due date: {item.due_date.strftime('%Y-%m-%d')}"
                else:
                    return f"Sorry, '{item.name}' is currently borrowed by someone else."
        return "Item not found."

    def return_item(self, isbn_code, username):
        if username not in self.users_data:
            return "Invalid username. Please log in first."

        for item in self.items:
            if item.isbn_code == isbn_code:
                if item.is_borrowed:
                    if item.due_date and item.due_date < datetime.datetime.now():
                        return f"'{item.name}' is overdue! Please return it as soon as possible."
                    item.return_item()
                    return f"'{item.name}' has been returned successfully."
                else:
                    return f"'{item.name}' was not borrowed."
        return "Item not found."

    def list_available_items(self):
        available_items = [item for item in self.items if not item.is_borrowed]
        if available_items:
            return "\n".join([str(item) for item in available_items])
        return "No items are available for borrowing."

    def search_items(self, query):
        found_items = [item for item in self.items if query.lower() in item.name.lower() or query.lower() in item.creator.lower()]
        if found_items:
            return "\n".join([str(item) for item in found_items])
        return f"No items found matching '{query}'."

    def authenticate(self, username, password):
        if self.users_data.get(username) == password:
            return True
        return False


class LibraryApp:
    def __init__(self, root, library_system):
        self.root = root
        self.library_system = library_system
        self.logged_in_user = None

        self.root.title("Library Management System")
        self.root.geometry("1000x800")
        self.root.config(bg="beige")

        self.heading_label = tk.Label(root, text="Library Management System", font=("Arial", 24, "bold"), fg="maroon", bg="beige")
        self.heading_label.pack(pady=20)

        self.heading_label = tk.Label(root, text="BookWorx: Your Digital Library, Simplified", font=("Arial", 18, "bold"), fg="maroon", bg="beige")
        self.heading_label.pack(pady=10)

        self.username_label = tk.Label(root, text="Username", font=("Times New Roman", 12), bg="beige")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, font=("Times New Roman", 12))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Password", font=("Times New Roman", 12), bg="beige")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*", font=("Times New Roman", 12))
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Login", font=("Times New Roman", 12), bg="#4CAF50", fg="white", command=self.login)
        self.login_button.pack(pady=10)

        self.add_button = tk.Button(root, text="Add a Book", font=("Times New Roman", 12), bg="#FF6347", fg="white", command=self.add_book)
        self.add_button.pack(pady=5)

        self.borrow_button = tk.Button(root, text="Borrow a Book", font=("Times New Roman", 12), bg="#00BFFF", fg="white", command=self.borrow_book)
        self.borrow_button.pack(pady=5)

        self.return_button = tk.Button(root, text="Return a Book", font=("Times New Roman", 12), bg="#FF4500", fg="white", command=self.return_book)
        self.return_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Available Books", font=("Times New Roman", 12), bg="#32CD32", fg="white", command=self.view_books)
        self.view_button.pack(pady=5)

        self.search_button = tk.Button(root, text="Search for an Item", font=("Times New Roman", 12), bg="#8A2BE2", fg="white", command=self.search_item)
        self.search_button.pack(pady=5)

        self.logout_button = tk.Button(root, text="Logout", font=("Times New Roman", 12), bg="#607D8B", fg="white", command=self.logout)
        self.logout_button.pack(pady=10)

        self.output_text = tk.Text(root, height=10, width=60, font=("Times New Roman", 12))
        self.output_text.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.library_system.authenticate(username, password):
            self.logged_in_user = username
            messagebox.showinfo("Login", "Login successful!")
            self.show_book_management_ui()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def show_book_management_ui(self):
        self.username_entry.config(state=tk.DISABLED)
        self.password_entry.config(state=tk.DISABLED)
        self.login_button.config(state=tk.DISABLED)

    def logout(self):
        self.logged_in_user = None
        self.username_entry.config(state=tk.NORMAL)
        self.password_entry.config(state=tk.NORMAL)
        self.login_button.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        messagebox.showinfo("Logout", "You have successfully logged out.")

    def add_book(self):
        self.output_text.delete(1.0, tk.END)
        name = self.ask_user_input("Enter item name: ")
        creator = self.ask_user_input("Enter creator: ")
        isbn_code = self.ask_user_input("Enter ISBN code: ")
        message = self.library_system.add_item(name, creator, isbn_code)
        self.output_text.insert(tk.END, message)

    def borrow_book(self):
        self.output_text.delete(1.0, tk.END)
        isbn_code = self.ask_user_input("Enter ISBN code of the item to borrow: ")
        message = self.library_system.borrow_item(isbn_code, self.logged_in_user)
        self.output_text.insert(tk.END, message)

    def return_book(self):
        self.output_text.delete(1.0, tk.END)
        isbn_code = self.ask_user_input("Enter ISBN code of the item to return: ")
        message = self.library_system.return_item(isbn_code, self.logged_in_user)
        self.output_text.insert(tk.END, message)

    def view_books(self):
        self.output_text.delete(1.0, tk.END)
        message = self.library_system.list_available_items()
        self.output_text.insert(tk.END, message)

    def search_item(self):
        self.output_text.delete(1.0, tk.END)
        query = self.ask_user_input("Enter item name or creator to search: ")
        message = self.library_system.search_items(query)
        self.output_text.insert(tk.END, message)

    def ask_user_input(self, prompt):
        input_window = tk.Toplevel(self.root)
        input_window.title(prompt)

        label = tk.Label(input_window, text=prompt, font=("Times New Roman", 12))
        label.pack()

        input_field = tk.Entry(input_window, font=("Times New Roman", 12))
        input_field.pack(pady=5)

        submit_button = tk.Button(input_window, text="Submit", font=("Times New Roman", 12), command=lambda: self.close_input_window(input_window, input_field))
        submit_button.pack(pady=5)

        self.root.wait_window(input_window)
        return self.user_input

    def close_input_window(self, input_window, input_field):
        self.user_input = input_field.get()
        input_window.destroy()


def main():
    library_system = LibrarySystem()
    root = tk.Tk()
    app = LibraryApp(root, library_system)
    root.mainloop()


if __name__ == "__main__":
    main()
