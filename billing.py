import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta
import random

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing & Invoice Management System")
        self.root.geometry("950x600")
        self.root.configure(bg="#f5f5f5")

        # Variables
        self.items = []
        self.total = 0
        self.gst_rate = 0.18
        self.order_id = self.generate_order_id()

        # ---------------- Header with Logo ----------------
        header_frame = tk.Frame(root, bg="#1e3d59")
        header_frame.pack(fill="x")

        try:
            logo_img = Image.open("asserts/logo.ico")
            logo_img = logo_img.resize((60, 60))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(header_frame, image=self.logo, bg="#1e3d59").pack(side="left", padx=10, pady=5)
        except:
            pass

        tk.Label(header_frame, text=" Billing & Invoice System",
                 font=("Verdana", 22, "bold"), bg="#1e3d59", fg="#f5f5f5").pack(side="left", padx=10, pady=5)

        # ---------------- Product Entry ----------------
        entry_frame = tk.Frame(root, bg="#f5f5f5", padx=10, pady=10)
        entry_frame.pack(fill="x")

        tk.Label(entry_frame, text="Product Name:", font=("Verdana", 12), bg="#f5f5f5").grid(row=0, column=0)
        self.product_name = tk.Entry(entry_frame, font=("Verdana", 12), width=20)
        self.product_name.grid(row=0, column=1, padx=10)

        tk.Label(entry_frame, text="Quantity:", font=("Verdana", 12), bg="#f5f5f5").grid(row=0, column=2)
        self.qty = tk.Entry(entry_frame, font=("Verdana", 12), width=10)
        self.qty.grid(row=0, column=3, padx=10)

        tk.Label(entry_frame, text="Price:", font=("Verdana", 12), bg="#f5f5f5").grid(row=0, column=4)
        self.price = tk.Entry(entry_frame, font=("Verdana", 12), width=10)
        self.price.grid(row=0, column=5, padx=10)

        tk.Button(entry_frame, text="Add Item", command=self.add_item,
                  bg="#ff6f61", fg="white", font=("Verdana", 12, "bold"),
                  activebackground="#ff8566", activeforeground="white").grid(row=0, column=6, padx=10)

        # ---------------- Item Table ----------------
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Verdana", 12, "bold"), foreground="#1e3d59")
        style.configure("Treeview", font=("Verdana", 11), rowheight=25)
        style.map('Treeview', background=[('selected', '#aad4ff')])

        self.tree = ttk.Treeview(root, columns=("Name", "Qty", "Price", "Total"), show="headings", height=10)
        self.tree.heading("Name", text="Product")
        self.tree.heading("Qty", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Total", text="Total")
        self.tree.pack(padx=10, pady=10, fill="x")

        # ---------------- Total Label ----------------
        self.total_label = tk.Label(root, text="Total: ₹0.00",
                                    font=("Verdana", 14, "bold"), fg="#1e3d59", bg="#f5f5f5")
        self.total_label.pack()

        # ---------------- Buttons ----------------
        button_frame = tk.Frame(root, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Generate PDF Bill", command=self.generate_bill_pdf,
                  bg="#28a745", fg="white", font=("Verdana", 12, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Clear", command=self.clear_all,
                  bg="#dc3545", fg="white", font=("Verdana", 12, "bold")).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="View Sales Report", command=self.show_sales_report,
                  bg="#1e3d59", fg="white", font=("Verdana", 12, "bold")).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Clear Sales Data", command=self.clear_sales_data,
                  bg="#ffc107", fg="white", font=("Verdana", 12, "bold")).grid(row=0, column=3, padx=10)

    # --------------------- ADD ITEM ---------------------
    def add_item(self):
        name = self.product_name.get()
        qty = self.qty.get()
        price = self.price.get()

        if not name or not qty or not price:
            messagebox.showerror("Error", "Please enter all fields")
            return

        try:
            qty = int(qty)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price")
            return

        total = qty * price
        self.items.append((name, qty, price, total))
        self.tree.insert("", "end", values=(name, qty, price, total))

        self.total += total
        self.update_total_label()

        self.product_name.delete(0, tk.END)
        self.qty.delete(0, tk.END)
        self.price.delete(0, tk.END)

    # --------------------- UPDATE TOTAL ---------------------
    def update_total_label(self):
        gst_amount = self.total * self.gst_rate
        grand_total = self.total + gst_amount
        self.total_label.config(text=f"Subtotal: ₹{self.total:.2f} | GST(18%): ₹{gst_amount:.2f} | Grand Total: ₹{grand_total:.2f}")

    # --------------------- GENERATE ORDER ID ---------------------
    def generate_order_id(self):
        return f"ORD{random.randint(1000, 9999)}"

    # --------------------- GENERATE PDF BILL ---------------------
    def generate_bill_pdf(self):
        if not self.items:
            messagebox.showwarning("Warning", "No items to generate bill")
            return

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"invoice_{date}.pdf"

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawString(200, 800, "SHOP INVOICE")

        c.setFont("Helvetica", 12)
        c.drawString(50, 780, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        c.drawString(400, 780, f"Order ID: {self.order_id}")
        c.line(50, 775, 550, 775)

        y = 750
        c.drawString(50, y, "Product")
        c.drawString(250, y, "Qty")
        c.drawString(320, y, "Price")
        c.drawString(400, y, "Total")
        c.line(50, y - 5, 550, y - 5)

        y -= 20
        for name, qty, price, total in self.items:
            c.drawString(50, y, str(name))
            c.drawString(260, y, str(qty))
            c.drawString(320, y, f"₹{price:.2f}")
            c.drawString(400, y, f"₹{total:.2f}")
            y -= 20

        c.line(50, y, 550, y)
        y -= 20

        gst_amount = self.total * self.gst_rate
        grand_total = self.total + gst_amount

        c.drawString(50, y, f"Subtotal: ₹{self.total:.2f}")
        y -= 20
        c.drawString(50, y, f"GST (18%): ₹{gst_amount:.2f}")
        y -= 20
        c.drawString(50, y, f"Grand Total: ₹{grand_total:.2f}")

        c.save()
        messagebox.showinfo("Success", f"Invoice generated: {filename}")

        # Record sales with order_id
        with open("sales_report.txt", "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d')},{self.order_id},{self.total},{gst_amount},{grand_total}\n")

        # Reset for next order
        self.items.clear()
        self.tree.delete(*self.tree.get_children())
        self.total = 0
        self.update_total_label()
        self.order_id = self.generate_order_id()

    # --------------------- CLEAR ALL ---------------------
    def clear_all(self):
        self.items.clear()
        self.tree.delete(*self.tree.get_children())
        self.total = 0
        self.update_total_label()

    # --------------------- CLEAR SALES DATA ---------------------
    def clear_sales_data(self):
        if os.path.exists("sales_report.txt"):
            open("sales_report.txt", "w").close()
            messagebox.showinfo("Success", "Sales report cleared!")
        else:
            messagebox.showinfo("Info", "No sales report file found.")

    # --------------------- SALES REPORT ---------------------
    def show_sales_report(self):
        if not os.path.exists("sales_report.txt"):
            messagebox.showinfo("No Data", "No sales data found.")
            return

        report_window = tk.Toplevel(self.root)
        report_window.title("Sales Report")
        report_window.geometry("650x450")
        report_window.configure(bg="#f5f5f5")

        # Period selection
        period_frame = tk.Frame(report_window, bg="#f5f5f5")
        period_frame.pack(pady=10)

        tk.Label(period_frame, text="View Report:", font=("Verdana", 12), bg="#f5f5f5").pack(side="left", padx=5)
        period_var = tk.StringVar(value="Daily")
        period_options = ["Daily", "Weekly", "Monthly"]
        period_menu = ttk.Combobox(period_frame, textvariable=period_var, values=period_options, state="readonly")
        period_menu.pack(side="left", padx=5)

        tk.Label(period_frame, text="Select Date:", font=("Verdana", 12), bg="#f5f5f5").pack(side="left", padx=5)
        date_var = tk.StringVar()
        date_entry = DateEntry(period_frame, textvariable=date_var, date_pattern="yyyy-mm-dd")
        date_entry.pack(side="left", padx=5)

        # Treeview
        tree = ttk.Treeview(report_window, columns=("Date", "OrderID", "Subtotal", "GST", "Total"), show="headings", height=15)
        tree.heading("Date", text="Date")
        tree.heading("OrderID", text="Order ID")
        tree.heading("Subtotal", text="Subtotal")
        tree.heading("GST", text="GST")
        tree.heading("Total", text="Total")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Function to load filtered data
        def load_data(*args):
            tree.delete(*tree.get_children())
            filter_option = period_var.get()
            today = datetime.now().date()

            selected_date = None
            if date_var.get():
                try:
                    selected_date = datetime.strptime(date_var.get(), "%Y-%m-%d").date()
                except:
                    selected_date = None

            with open("sales_report.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) != 5:
                        continue  # skip invalid lines
                    date_str, order_id, subtotal, gst, total = parts
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                    add_row = False

                    if selected_date:
                        if date_obj == selected_date:
                            add_row = True
                    else:
                        if filter_option == "Daily" and date_obj == today:
                            add_row = True
                        elif filter_option == "Weekly" and (today - date_obj).days < 7:
                            add_row = True
                        elif filter_option == "Monthly" and today.month == date_obj.month and today.year == date_obj.year:
                            add_row = True

                    if add_row:
                        tree.insert("", "end", values=(date_str, order_id, subtotal, gst, total))

        # Bind combobox and date picker
        period_menu.bind("<<ComboboxSelected>>", load_data)
        date_entry.bind("<<DateEntrySelected>>", load_data)

        # Load initial data
        load_data()

# --------------------- MAIN DRIVER ---------------------
if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("asserts/logo.ico")
    except:
        pass
    app = BillingSystem(root)
    root.mainloop()
