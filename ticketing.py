import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

# -------------------------------
# DATABASE LAYER (LOCAL STORAGE)
# -------------------------------
class TicketDB:
    def __init__(self, db_name="tickets.db"):
        self.db_path = os.path.join(os.getcwd(), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def create_ticket(self, title, description, category, priority):
        query = """
        INSERT INTO tickets (title, description, category, priority, status, created_at)
        VALUES (?, ?, ?, ?, 'Open', ?)
        """
        self.conn.execute(
            query,
            (
                title,
                description,
                category,
                priority,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        self.conn.commit()

    def get_tickets(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
        return cursor.fetchall()

    def update_status(self, ticket_id, status):
        self.conn.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (status, ticket_id)
        )
        self.conn.commit()

    def delete_ticket(self, ticket_id):
        self.conn.execute(
            "DELETE FROM tickets WHERE id = ?",
            (ticket_id,)
        )
        self.conn.commit()


# -------------------------------
# APPLICATION UI
# -------------------------------
class TicketingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Ticketing System")
        self.root.geometry("950x520")

        self.db = TicketDB()

        self.build_ui()
        self.load_tickets()

    # -------------------------------
    # UI SETUP
    # -------------------------------
    def build_ui(self):
        form_frame = ttk.LabelFrame(self.root, text="Create Ticket")
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        list_frame = ttk.LabelFrame(self.root, text="Tickets (Stored Locally)")
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Form Fields ---
        ttk.Label(form_frame, text="Title").pack(anchor=tk.W)
        self.title_entry = ttk.Entry(form_frame, width=30)
        self.title_entry.pack(pady=3)

        ttk.Label(form_frame, text="Description").pack(anchor=tk.W)
        self.desc_text = tk.Text(form_frame, width=30, height=6)
        self.desc_text.pack(pady=3)

        ttk.Label(form_frame, text="Category").pack(anchor=tk.W)
        self.category_combo = ttk.Combobox(
            form_frame,
            values=["IT Support", "Customer Support", "Billing", "General"],
            state="readonly"
        )
        self.category_combo.pack(pady=3)
        self.category_combo.set("General")

        ttk.Label(form_frame, text="Priority").pack(anchor=tk.W)
        self.priority_combo = ttk.Combobox(
            form_frame,
            values=["Low", "Medium", "High", "Critical"],
            state="readonly"
        )
        self.priority_combo.pack(pady=3)
        self.priority_combo.set("Medium")

        ttk.Button(
            form_frame,
            text="Create Ticket",
            command=self.create_ticket
        ).pack(pady=12)

        # --- Ticket Table ---
        columns = ("ID", "Title", "Category", "Priority", "Status", "Created")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # --- Actions ---
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=6)

        ttk.Label(action_frame, text="Status:").pack(side=tk.LEFT)

        self.status_combo = ttk.Combobox(
            action_frame,
            values=["Open", "In Progress", "Closed"],
            state="readonly",
            width=15
        )
        self.status_combo.pack(side=tk.LEFT, padx=5)
        self.status_combo.set("Open")

        ttk.Button(
            action_frame,
            text="Update Status",
            command=self.update_ticket_status
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            action_frame,
            text="Delete Ticket",
            command=self.delete_ticket
        ).pack(side=tk.RIGHT, padx=5)

    # -------------------------------
    # APPLICATION LOGIC
    # -------------------------------
    def create_ticket(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not title or not description:
            messagebox.showerror("Validation Error", "Title and Description are required.")
            return

        self.db.create_ticket(
            title,
            description,
            self.category_combo.get(),
            self.priority_combo.get()
        )

        self.clear_form()
        self.load_tickets()

    def load_tickets(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for ticket in self.db.get_tickets():
            self.tree.insert("", tk.END, values=ticket)

    def update_ticket_status(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Select a ticket to update.")
            return

        ticket_id = self.tree.item(selected)["values"][0]
        self.db.update_status(ticket_id, self.status_combo.get())
        self.load_tickets()

    def delete_ticket(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Select a ticket to delete.")
            return

        ticket_id = self.tree.item(selected)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete ticket #{ticket_id}?"
        )

        if confirm:
            self.db.delete_ticket(ticket_id)
            self.load_tickets()

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.category_combo.set("General")
        self.priority_combo.set("Medium")


# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicketingApp(root)
    root.mainloop()
