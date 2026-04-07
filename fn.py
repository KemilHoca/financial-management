import tkinter as tk
from tkinter import messagebox

customers = []

# ------------------ RISK ------------------
def calculate_risk(balance, delay):
    if balance > 50000 or delay > 30:
        return "High"
    elif balance > 20000 or delay > 15:
        return "Medium"
    return "Low"

# ------------------ ADD ------------------
def add_customer():
    try:
        name = entry_name.get()
        company = entry_company.get()
        balance = float(entry_balance.get())
        delay = int(entry_delay.get())
        project = int(entry_project.get())

        risk = calculate_risk(balance, delay)

        customer = {
            "name": name,
            "company": company,
            "balance": balance,
            "delay": delay,
            "project": project,
            "risk": risk
        }

        customers.append(customer)

        render_list()
        render_dashboard()

        messagebox.showinfo("Başarılı", "Müşteri eklendi")

    except:
        messagebox.showerror("Hata", "Geçersiz veri")

# ------------------ CLEAR ------------------
def clear_form():
    entry_name.delete(0, tk.END)
    entry_company.delete(0, tk.END)
    entry_balance.delete(0, tk.END)
    entry_delay.delete(0, tk.END)
    entry_project.delete(0, tk.END)

# ------------------ TEST DATA ------------------
def load_test():
    test_data = [
        ("Ali", "ABC", 10000, 5, 2),
        ("Veli", "XYZ", 30000, 20, 1),
        ("Ayşe", "QWE", 60000, 40, 3)
    ]

    for t in test_data:
        risk = calculate_risk(t[2], t[3])
        customers.append({
            "name": t[0],
            "company": t[1],
            "balance": t[2],
            "delay": t[3],
            "project": t[4],
            "risk": risk
        })

    render_list()
    render_dashboard()

# ------------------ LIST ------------------
def render_list():
    listbox.delete(0, tk.END)
    for c in customers:
        listbox.insert(tk.END,
            f"{c['name']} - {c['company']} | Bakiye:{c['balance']} | Gecikme:{c['delay']} | Risk:{c['risk']}"
        )

# ------------------ DASHBOARD ------------------
def render_dashboard():
    total = len(customers)
    high = medium = low = 0
    total_balance = 0
    max_balance = 0
    max_delay = 0

    for c in customers:
        if c["risk"] == "High":
            high += 1
        elif c["risk"] == "Medium":
            medium += 1
        else:
            low += 1

        total_balance += c["balance"]
        max_balance = max(max_balance, c["balance"])
        max_delay = max(max_delay, c["delay"])

    avg = total_balance / total if total else 0

    dashboard_label.config(text=
        f"Toplam: {total} | High: {high} | Medium: {medium} | Low: {low} | "
        f"Ortalama: {avg:.2f} | Max Bakiye: {max_balance} | Max Gecikme: {max_delay}"
    )

# ------------------ UI ------------------
root = tk.Tk()
root.title("Customer Management")
root.geometry("700x600")

# FORM
tk.Label(root, text="Customer Entry Form", font=("Arial", 14)).pack()

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Müşteri Adı").grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Firma Adı").grid(row=1, column=0)
entry_company = tk.Entry(frame)
entry_company.grid(row=1, column=1)

tk.Label(frame, text="Açık Bakiye").grid(row=2, column=0)
entry_balance = tk.Entry(frame)
entry_balance.grid(row=2, column=1)

tk.Label(frame, text="Gecikme Günü").grid(row=3, column=0)
entry_delay = tk.Entry(frame)
entry_delay.grid(row=3, column=1)

tk.Label(frame, text="Aktif Proje Sayısı").grid(row=4, column=0)
entry_project = tk.Entry(frame)
entry_project.grid(row=4, column=1)

# BUTTONS
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Müşteri Ekle", command=add_customer).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Formu Temizle", command=clear_form).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Test Veri Yükle", command=load_test).grid(row=0, column=2, padx=5)

# LIST
tk.Label(root, text="Customer List", font=("Arial", 12)).pack()
listbox = tk.Listbox(root, width=100)
listbox.pack(pady=10)

# DASHBOARD
tk.Label(root, text="Dashboard", font=("Arial", 12)).pack()
dashboard_label = tk.Label(root, text="")
dashboard_label.pack()

root.mainloop()