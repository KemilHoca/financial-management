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

# ------------------ VALIDATION ------------------
def validate_input(name, company, balance, delay, project):
    if not name:
        return "Müşteri adı boş"
    if not company:
        return "Firma adı boş"
    if balance < 0 or delay < 0 or project < 0:
        return "Negatif değer girilemez"
    return None

# ------------------ ADD ------------------
def add_customer():
    try:
        name = entry_name.get().strip()
        company = entry_company.get().strip()
        balance = float(entry_balance.get())
        delay = int(entry_delay.get())
        project = int(entry_project.get())

        error = validate_input(name, company, balance, delay, project)
        if error:
            messagebox.showerror("Hata", error)
            return

        risk = calculate_risk(balance, delay)

        customers.append({
            "name": name,
            "company": company,
            "balance": balance,
            "delay": delay,
            "project": project,
            "risk": risk
        })

        render_list()
        render_dashboard()
        messagebox.showinfo("Başarılı", "Müşteri eklendi")

    except:
        messagebox.showerror("Hata", "Geçersiz veri")

# ------------------ CLEAR ------------------
def clear_form():
    for e in [entry_name, entry_company, entry_balance, entry_delay, entry_project]:
        e.delete(0, tk.END)

# ------------------ TEST DATA ------------------
def load_test():
    test_data = [
        ("Ali", "ABC", 10000, 5, 2),
        ("Veli", "XYZ", 30000, 20, 1),
        ("Ayşe", "QWE", 60000, 40, 3)
    ]

    for t in test_data:
        customers.append({
            "name": t[0],
            "company": t[1],
            "balance": t[2],
            "delay": t[3],
            "project": t[4],
            "risk": calculate_risk(t[2], t[3])
        })

    render_list()
    render_dashboard()
    messagebox.showinfo("Bilgi", "Test verisi yüklendi")

# ------------------ LIST ------------------
def render_list():
    listbox.delete(0, tk.END)

    # HEADER
    listbox.insert(tk.END, "Ad | Firma | Bakiye | Gecikme | Risk")
    listbox.insert(tk.END, "-"*60)

    for c in customers:
        listbox.insert(tk.END,
            f"{c['name']} | {c['company']} | {c['balance']} | {c['delay']} | {c['risk']}"
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
        f"""
Toplam Müşteri: {total}
High Risk: {high}
Medium Risk: {medium}
Low Risk: {low}

Ortalama Bakiye: {avg:.2f}
En Yüksek Bakiye: {max_balance}
En Uzun Gecikme: {max_delay}
"""
    )

# ------------------ UI ------------------
root = tk.Tk()
root.title("Customer Management")
root.geometry("750x650")

# TITLE
tk.Label(root, text="Customer Entry Form", font=("Arial", 16)).pack(pady=10)

# FORM FRAME
frame = tk.Frame(root)
frame.pack()

labels = [
    "Müşteri Adı",
    "Firma Adı",
    "Açık Bakiye",
    "Gecikme Günü",
    "Aktif Proje Sayısı"
]

entries = []

for i, text in enumerate(labels):
    tk.Label(frame, text=text, width=20, anchor="w").grid(row=i, column=0, padx=5, pady=5)
    e = tk.Entry(frame, width=30)
    e.grid(row=i, column=1, padx=5, pady=5)
    entries.append(e)

entry_name, entry_company, entry_balance, entry_delay, entry_project = entries

# BUTTONS
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Müşteri Ekle", width=15, command=add_customer).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Formu Temizle", width=15, command=clear_form).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Test Veri Yükle", width=15, command=load_test).grid(row=0, column=2, padx=5)

# LIST
tk.Label(root, text="Customer List", font=("Arial", 14)).pack()
listbox = tk.Listbox(root, width=100, height=10)
listbox.pack(pady=10)

# DASHBOARD
tk.Label(root, text="Dashboard", font=("Arial", 14)).pack()
dashboard_label = tk.Label(root, justify="left", font=("Arial", 11))
dashboard_label.pack()

root.mainloop()
