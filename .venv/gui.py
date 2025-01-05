import tkinter as tk
from tkinter import ttk, messagebox
from database import create_database, load_contacts_to_list, update_contact_in_db
from gui_functions import refresh_contacts, add_contact, delete_contact


def main():
    create_database()
    contact_list = load_contacts_to_list()

    root = tk.Tk()
    root.title("Menadżer kontaktów")

    # Contacts table
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tree = ttk.Treeview(frame, columns=("ID", "Imię", "Nazwisko", "Telefon", "Email"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Imię", text="Imię")
    tree.heading("Nazwisko", text="Nazwisko")
    tree.heading("Telefon", text="Telefon")
    tree.heading("Email", text="Email")
    tree.pack(side=tk.LEFT)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Window for adding new contact
    def add_contact_window():
        add_window = tk.Toplevel(root)
        add_window.title("Dodaj kontakt")

        tk.Label(add_window, text="Imię").grid(row=0, column=0)
        entry_first_name = tk.Entry(add_window)
        entry_first_name.grid(row=0, column=1)

        tk.Label(add_window, text="Nazwisko").grid(row=1, column=0)
        entry_last_name = tk.Entry(add_window)
        entry_last_name.grid(row=1, column=1)

        tk.Label(add_window, text="Telefon").grid(row=2, column=0)
        entry_phone = tk.Entry(add_window)
        entry_phone.grid(row=2, column=1)

        tk.Label(add_window, text="Email").grid(row=3, column=0)
        entry_email = tk.Entry(add_window)
        entry_email.grid(row=3, column=1)

        tk.Button(add_window, text="Zapisz", command=lambda: add_contact(
            add_window, contact_list, tree, entry_first_name.get(), entry_last_name.get(),
            entry_phone.get(), entry_email.get())).grid(row=4, column=0, columnspan=2)

    # Logic for editing selected contact
    # TODO: Move to separate module
    def edit_selected_contact():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Błąd", "Nie wybrano kontaktu do edycji.")
            return

        contact_id = int(selected_item)
        current = contact_list.head
        while current:
            if current.contact_id == contact_id:
                break
            current = current.next

        if not current:
            messagebox.showerror("Błąd", "Nie znaleziono kontaktu.")
            return

        def save_edited_contact():
            new_first_name = entry_first_name.get()
            new_last_name = entry_last_name.get()
            new_phone_number = entry_phone.get()
            new_email = entry_email.get()

            if not new_first_name or not new_last_name or not new_phone_number:
                messagebox.showerror("Błąd", "Wszystkie pola oprócz email są wymagane.")
                return

            # Update in DB
            update_contact_in_db(contact_id, new_first_name, new_last_name, new_phone_number, new_email)

            # Update in the list
            current.first_name = new_first_name
            current.last_name = new_last_name
            current.phone_number = new_phone_number
            current.email = new_email

            refresh_contacts(tree, contact_list)
            edit_window.destroy()
            messagebox.showinfo("Sukces", "Kontakt został zaktualizowany.")

        # Edit contact window
        edit_window = tk.Toplevel(root)
        edit_window.title("Edytuj kontakt")

        tk.Label(edit_window, text="Imię").grid(row=0, column=0)
        entry_first_name = tk.Entry(edit_window)
        entry_first_name.grid(row=0, column=1)
        entry_first_name.insert(0, current.first_name)

        tk.Label(edit_window, text="Nazwisko").grid(row=1, column=0)
        entry_last_name = tk.Entry(edit_window)
        entry_last_name.grid(row=1, column=1)
        entry_last_name.insert(0, current.last_name)

        tk.Label(edit_window, text="Numer telefonu").grid(row=2, column=0)
        entry_phone = tk.Entry(edit_window)
        entry_phone.grid(row=2, column=1)
        entry_phone.insert(0, current.phone_number)

        tk.Label(edit_window, text="Email").grid(row=3, column=0)
        entry_email = tk.Entry(edit_window)
        entry_email.grid(row=3, column=1)
        entry_email.insert(0, current.email)

        tk.Button(edit_window, text="Zapisz", command=save_edited_contact).grid(row=4, column=0, columnspan=2)

    def search_contacts():
        query = entry_search.get().lower()
        if not query:
            messagebox.showwarning("Uwaga", "Pole wyszukiwania jest puste.")
            return

        tree.delete(*tree.get_children())  # Clear whole table
        current = contact_list.head
        while current:
            if (query in current.first_name.lower() or
                    query in current.last_name.lower() or
                    query in current.phone_number.lower() or
                    (current.email and query in current.email.lower())):
                # Add contacts that match for specific search
                tree.insert("", "end", iid=current.contact_id, values=(
                    current.contact_id,
                    current.first_name,
                    current.last_name,
                    current.phone_number,
                    current.email
                ))
            current = current.next

        if not tree.get_children():
            messagebox.showinfo("Informacja", "Nie znaleziono kontaktów pasujących do zapytania.")

    def reset_search():
        entry_search.delete(0, tk.END)  # Clear search field
        refresh_contacts(tree, contact_list)  # Reset whole list

    # Logic for deleting selected contact
    def delete_selected_contact():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Błąd", "Nie wybrano kontaktu do usunięcia.")
            return

        contact_id = int(selected_item)
        delete_contact(contact_list, tree, contact_id)

    # Search field and search + reset button
    # TODO: Move to separate module
    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Szukaj:").grid(row=0, column=0)
    entry_search = tk.Entry(search_frame, width=30)
    entry_search.grid(row=0, column=1, padx=5)

    tk.Button(search_frame, text="Wyszukaj", command=search_contacts).grid(row=0, column=2, padx=5)
    tk.Button(search_frame, text="Resetuj", command=reset_search).grid(row=0, column=3, padx=5)

    # Buttons for managing contacts
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Dodaj kontakt", command=add_contact_window).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Usuń kontakt", command=delete_selected_contact).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Edytuj kontakt", command=edit_selected_contact).grid(row=0, column=2, padx=5)

    refresh_contacts(tree, contact_list)
    root.mainloop()


if __name__ == "__main__":
    main()
