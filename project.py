import csv
import os
import calendar
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

FILENAME = "subscriptions.csv"

def main():
    # Ensure database file exists on startup
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Start Date", "Price", "Currency", "Cycle"])

    # 1. Main Root Configuration
    root = tk.Tk()
    root.title("Subscription Monitor")
    root.geometry("940x740") 
    root.configure(bg="#141414")  
    root.resizable(False, False)

    # 2. UI Theme Style Customization
    style = ttk.Style()
    style.theme_use("clam") 
    
    style.configure("TCombobox", fieldbackground="#2b2b2b", background="#3a3a3a", foreground="white", bordercolor="#1e1e1e", arrowcolor="white")
    style.map("TCombobox", fieldbackground=[("readonly", "#2b2b2b")], selectbackground=[("readonly", "#a370f7")], selectforeground=[("readonly", "white")])
    
    style.configure("Treeview", background="#1e1e1e", fieldbackground="#1e1e1e", foreground="#ffffff", rowheight=28, borderwidth=0, font=("Helvetica", 9))
    style.configure("Treeview.Heading", background="#2d2d2d", foreground="#a370f7", font=("Helvetica", 9, "bold"), borderwidth=0)
    style.map("Treeview.Heading", background=[('active', '#593196')])

    # --- TOP HEADER BANNER ---
    header_frame = tk.Frame(root, bg="#1e1e1e", height=60)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(header_frame, text="📊 SUBSCRIPTION MONITOR DASHBOARD", font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#1e1e1e")
    title_label.pack(side="left", padx=20, pady=18)

    # --- MAIN SPLIT WORKSPACE CONTAINER ---
    workspace = tk.Frame(root, bg="#141414")
    workspace.pack(fill="both", expand=True, padx=20, pady=10)

    # LEFT PANEL: Control Inputs & Table
    left_panel = tk.Frame(workspace, bg="#141414")
    left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

    input_card = tk.LabelFrame(left_panel, text=" Track New Subscription ", font=("Helvetica", 10, "bold"), fg="#a370f7", bg="#1e1e1e", bd=0, padx=15, pady=15)
    input_card.pack(fill="x", pady=(5, 10))

    # Grid Construction For Input Fields
    tk.Label(input_card, text="App Name:", font=("Helvetica", 9), fg="#b3b3b3", bg="#1e1e1e").grid(row=0, column=0, sticky="w", pady=6)
    name_entry = tk.Entry(input_card, font=("Helvetica", 10), bg="#2b2b2b", fg="white", insertbackground="white", bd=0, width=22)
    name_entry.grid(row=0, column=1, columnspan=3, sticky="w", padx=5, pady=6)

    tk.Label(input_card, text="Start Date:", font=("Helvetica", 9), fg="#b3b3b3", bg="#1e1e1e").grid(row=1, column=0, sticky="w", pady=6)
    
    years = [str(y) for y in range(2020, 2031)]
    months = [f"{m:02d}" for m in range(1, 13)]
    days = [f"{d:02d}" for d in range(1, 32)]

    year_combo = ttk.Combobox(input_card, values=years, width=5, state="readonly")
    year_combo.set(str(datetime.today().year))
    year_combo.grid(row=1, column=1, padx=2, pady=6)

    month_combo = ttk.Combobox(input_card, values=months, width=4, state="readonly")
    month_combo.set(f"{datetime.today().month:02d}")
    month_combo.grid(row=1, column=2, padx=2, pady=6)

    day_combo = ttk.Combobox(input_card, values=days, width=4, state="readonly")
    day_combo.set(f"{datetime.today().day:02d}")
    day_combo.grid(row=1, column=3, padx=2, pady=6)

    tk.Label(input_card, text="Cost Value:", font=("Helvetica", 9), fg="#b3b3b3", bg="#1e1e1e").grid(row=2, column=0, sticky="w", pady=6)
    price_entry = tk.Entry(input_card, font=("Helvetica", 10), bg="#2b2b2b", fg="white", insertbackground="white", bd=0, width=10)
    price_entry.grid(row=2, column=1, sticky="w", padx=5, pady=6)

    currency_combo = ttk.Combobox(input_card, values=["$ (USD)", "₹ (INR)", "¥ (CNY)", "€ (EUR)", "£ (GBP)"], width=8, state="readonly")
    currency_combo.set("$ (USD)")
    currency_combo.grid(row=2, column=2, columnspan=2, sticky="w", padx=5, pady=6)

    tk.Label(input_card, text="Interval:", font=("Helvetica", 9), fg="#b3b3b3", bg="#1e1e1e").grid(row=3, column=0, sticky="w", pady=6)
    cycle_combo = ttk.Combobox(input_card, values=["monthly", "yearly"], width=12, state="readonly")
    cycle_combo.set("monthly")
    cycle_combo.grid(row=3, column=1, columnspan=2, sticky="w", padx=5, pady=6)

    # RIGHT PANEL: Critical Notifications Alert Window
    right_panel = tk.Frame(workspace, bg="#141414", width=300)
    right_panel.pack(side="right", fill="both", padx=(10, 0))
    right_panel.pack_propagate(False)

    alert_card = tk.LabelFrame(right_panel, text=" ⚠️ CRITICAL ALERTS (NEXT 10 DAYS) ", font=("Helvetica", 10, "bold"), fg="#ff4d4d", bg="#1e1e1e", bd=0, padx=10, pady=10)
    alert_card.pack(fill="both", expand=True, pady=5)

    alert_box = tk.Text(alert_card, font=("Consolas", 10), bg="#1a1a1a", fg="#ff4d4d", bd=0, padx=8, pady=8, state="disabled")
    alert_box.pack(fill="both", expand=True)

    # --- MIDDLE SYSTEM TABLE LIST ---
    table_frame = tk.Frame(left_panel, bg="#1e1e1e")
    table_frame.pack(fill="both", expand=True, pady=(5, 0))

    columns = ("name", "start", "cost", "cycle", "next_due", "remaining")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    
    tree.heading("name", text="SUBSCRIPTION")
    tree.heading("start", text="START DATE")
    tree.heading("cost", text="COST")
    tree.heading("cycle", text="INTERVAL")
    tree.heading("next_due", text="NEXT DUE")
    tree.heading("remaining", text="REMAINING")
    
    tree.column("name", width=140, anchor="w")
    tree.column("start", width=85, anchor="center")
    tree.column("cost", width=85, anchor="center")
    tree.column("cycle", width=80, anchor="center")
    tree.column("next_due", width=90, anchor="center")
    tree.column("remaining", width=90, anchor="center")
    tree.pack(fill="both", expand=True)

    # --- NEW: TABLE CONTROLS FRAME (FOR DELETING) ---
    table_controls = tk.Frame(table_frame, bg="#1e1e1e")
    table_controls.pack(fill="x", pady=5)

    # --- BOTTOM FINANCIAL SUMMARY DASHBOARD ---
    summary_frame = tk.LabelFrame(root, text=" Financial Analytics Summary ", font=("Helvetica", 10, "bold"), fg="#03DAC6", bg="#1e1e1e", bd=0, padx=15, pady=15)
    summary_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))

    summary_text = tk.Text(summary_frame, height=3, font=("Consolas", 10), bg="#1e1e1e", fg="#ffffff", bd=0, state="disabled")
    summary_text.pack(fill="both", expand=True)

    # --- UI BACKEND LOGIC SYNC HUB ---

    def refresh_dashboard():
        """Updates standard data visualization views along with the high-priority Alert logs and Analytics."""
        for item in tree.get_children():
            tree.delete(item)
            
        subs = load_subscriptions(FILENAME)
        today = datetime.today().date()
        
        for s in subs:
            next_date = calculate_next_due(s["start_date"], s["cycle"], today)
            days_left = (next_date - today).days
            timeline_str = f"{days_left} days left" if days_left > 0 else "Due Today"
            currency_symbol = s["currency"].split(" ")[0]
            
            tree.insert("", "end", values=(
                s["name"], s["start_date"], f"{currency_symbol} {s['price']:.2f}", 
                s["cycle"].upper(), next_date.strftime("%Y-%m-%d"), timeline_str
            ))
            
        alert_box.config(state="normal")
        alert_box.delete("1.0", tk.END)
        urgent_items = get_urgent_alerts(subs, today, horizon_days=10)
        
        if not urgent_items:
            alert_box.insert(tk.END, "✅ Perfect Check!\nNo accounts due inside\nthe next 10 days.")
        else:
            alert_box.insert(tk.END, "🚨 ACTION REQUIRED:\n" + "─" * 26 + "\n")
            for item in urgent_items:
                alert_box.insert(tk.END, f"• {item['name']}\n  Due: {item['date']} ({item['days_left']} days left)\n\n")
        alert_box.config(state="disabled")

        summary_text.config(state="normal")
        summary_text.delete("1.0", tk.END)
        analytics = calculate_financial_analytics(subs)
        
        if not analytics:
            summary_text.insert(tk.END, "No active subscriptions logged to calculate financial analytics.")
        else:
            stats_str = f"Total Active Subscriptions: {len(subs)} accounts\n" + "─" * 60 + "\n"
            for currency, totals in analytics.items():
                symbol = currency.split(" ")[0]
                stats_str += f"Total Yearly Burn ({symbol}): {symbol}{totals['yearly']:.2f}  |  Avg. Monthly: {symbol}{totals['monthly']:.2f}\n"
            summary_text.insert(tk.END, stats_str.strip())
        summary_text.config(state="disabled")

    def save_sub():
        """Validates inputs and saves new records."""
        constructed_date = f"{year_combo.get()}-{month_combo.get()}-{day_combo.get()}"
        try:
            clean_sub = validate_subscription(
                name_entry.get(), constructed_date, price_entry.get(), 
                currency_combo.get(), cycle_combo.get()
            )
            with open(FILENAME, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    clean_sub["name"], clean_sub["start_date"], 
                    clean_sub["price"], clean_sub["currency"], clean_sub["cycle"]
                ])
            
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            refresh_dashboard()
        except ValueError as e:
            messagebox.showerror("Input Alert", str(e))

    def delete_sub():
        """Identifies highlighted row, filters it out of the database, and rewrites the CSV."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please click on a subscription in the table to cancel it.")
            return
            
        item_data = tree.item(selected_item[0], "values")
        sub_name = item_data[0] # Grab the name from the highlighted row
        
        confirm = messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to permanently delete '{sub_name}' from your tracker?")
        if confirm:
            try:
                subs = load_subscriptions(FILENAME)
                updated_subs = remove_subscription(subs, sub_name)
                
                # Overwrite the CSV file with the updated list
                with open(FILENAME, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Name", "Start Date", "Price", "Currency", "Cycle"])
                    for s in updated_subs:
                        writer.writerow([s["name"], s["start_date"], s["price"], s["currency"], s["cycle"]])
                        
                refresh_dashboard()
                messagebox.showinfo("Deleted", f"'{sub_name}' was successfully removed.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    # --- ACTION BUTTONS ---
    tk.Button(
        input_card, text="➕ Save Tracker", command=save_sub, 
        font=("Helvetica", 9, "bold"), bg="#a370f7", fg="white", 
        activebackground="#593196", activeforeground="white", bd=0, width=14, height=2
    ).grid(row=0, column=4, rowspan=2, padx=20, pady=5)

    tk.Button(
        table_controls, text="🗑️ Cancel / Delete Selected", command=delete_sub, 
        font=("Helvetica", 9, "bold"), bg="#ff4d4d", fg="white", 
        activebackground="#cc0000", activeforeground="white", bd=0, width=24, height=1
    ).pack(side="right", padx=10, pady=5)

    refresh_dashboard()
    root.mainloop()


def load_subscriptions(filename):
    subscriptions = []
    if not os.path.exists(filename):
        return subscriptions
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            subscriptions.append({
                "name": row["Name"], "start_date": row["Start Date"],
                "price": float(row["Price"]), "currency": row["Currency"], "cycle": row["Cycle"]
            })
    return subscriptions


# --- CS50P REQUIRED INDEPENDENT BACKEND PROCESSING FUNCTIONS ---

def validate_subscription(name, date_str, price_str, currency_str, cycle_str):
    clean_name = name.strip().title()
    if not clean_name:
        raise ValueError("Subscription name cannot be left blank.")
        
    try:
        valid_date = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid calendar date. Ensure the month/day combination exists (e.g., no Feb 30th).")
        
    try:
        clean_price = round(float(price_str.strip()), 2)
        if clean_price < 0:
            raise ValueError
    except ValueError:
        raise ValueError("Price entries must be valid positive numbers.")
        
    return {
        "name": clean_name, "start_date": valid_date.strftime("%Y-%m-%d"),
        "price": clean_price, "currency": currency_str, "cycle": cycle_str
    }

def calculate_next_due(start_date_str, cycle, current_date):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    if start_date >= current_date:
        return start_date
        
    if cycle == "monthly":
        target = start_date
        while target < current_date:
            next_month = target.month + 1
            next_year = target.year
            if next_month > 12:
                next_month = 1
                next_year += 1
            max_days = calendar.monthrange(next_year, next_month)[1]
            target_day = min(start_date.day, max_days)
            target = datetime(next_year, next_month, target_day).date()
        return target
    else:
        target_year = current_date.year
        try:
            target = datetime(target_year, start_date.month, start_date.day).date()
        except ValueError:
            target = datetime(target_year, 2, 28).date()
        if target < current_date:
            try:
                target = datetime(target_year + 1, start_date.month, start_date.day).date()
            except ValueError:
                target = datetime(target_year + 1, 2, 28).date()
        return target

def get_urgent_alerts(subscriptions_list, current_date, horizon_days=10):
    urgent_alerts = []
    end_boundary = current_date + timedelta(days=horizon_days)
    for sub in subscriptions_list:
        next_bill = calculate_next_due(sub["start_date"], sub["cycle"], current_date)
        if current_date <= next_bill <= end_boundary:
            urgent_alerts.append({
                "name": sub["name"],
                "date": next_bill.strftime("%Y-%m-%d"),
                "days_left": (next_bill - current_date).days
            })
    urgent_alerts.sort(key=lambda x: x["date"])
    return urgent_alerts

def calculate_financial_analytics(subscriptions_list):
    analytics = {}
    for sub in subscriptions_list:
        currency = sub["currency"]
        if currency not in analytics:
            analytics[currency] = {"yearly": 0.0, "monthly": 0.0}
            
        yearly_cost = sub["price"] * 12 if sub["cycle"] == "monthly" else sub["price"]
        analytics[currency]["yearly"] += yearly_cost
        analytics[currency]["monthly"] += yearly_cost / 12
    return analytics

def remove_subscription(subscriptions_list, target_name):
    """Filters out the target subscription from the data list. Raises error if missing."""
    initial_length = len(subscriptions_list)
    
    # Keep everything that does NOT match the target name (case-insensitive)
    filtered_list = [sub for sub in subscriptions_list if sub["name"].lower() != target_name.lower()]
    
    if len(filtered_list) == initial_length:
        raise ValueError(f"Subscription '{target_name}' could not be located in the database.")
        
    return filtered_list

if __name__ == "__main__":
    main()