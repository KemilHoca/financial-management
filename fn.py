# fe.py
# Git Branch: frontend-dev (veya benzeri)

import tkinter as tk
from tkinter import messagebox

# ------------------ BRANCH UYUMU (MOCKING) ------------------
# Frontend henüz main'e merge edilmediyse ve be.py ortamda yoksa 
# kodun arayüz testleri için çökmesini engelliyoruz.
try:
    from be import Customer, CustomerManager
    print("Sistem: Gerçek Backend (be.py) bulundu ve yüklendi.")
except ImportError:
    print("Sistem UYARISI: be.py bulunamadı! Frontend branch'inde geliştirme yapılıyor varsayılıyor.")
    print("Sistem: Sahte (Mock) Backend ile devam ediliyor...\n")
    
    # Frontend'i test etmek için sahte sınıflar
    class Customer:
        def __init__(self, name, company, balance, delay_days, active_projects):
            self.name = name
            self.company = company
            self.balance = float(balance)
            self.delay_days = int(delay_days)
            self.active_projects = int(active_projects)
            self.risk_level = "MOCK RISK"
            self.status_note = "MOCK NOT"

    class CustomerManager:
        def __init__(self):
            self.customers = []
        def add_customer(self, customer):
            self.customers.append(customer)
        def get_all_customers(self):
            return self.customers
        def get_dashboard_data(self):
            return {
                "total": len(self.customers), "high": 0, "medium": 0, "low": len(self.customers),
                "avg": 999.99, "max_balance": 9999, "max_delay": 99
            }

# Yönetici nesnemizi başlatıyoruz
manager = CustomerManager()

# ------------------ FONKSİYONLAR ------------------
def add_customer():
    try:
        name = entry_name.get()
        company = entry_company.get()
        balance = float(entry_balance.get())
        delay = int(entry_delay.get())
        project = int(entry_project.get())

        new_customer = Customer(name, company, balance, delay, project)
        manager.add_customer(new_customer)

        render_list()
        render_dashboard()
        clear_form()

        messagebox.showinfo("Başarılı", f"{name} adlı müşteri eklendi.")
    except ValueError:
        messagebox.showerror("Hata", "Lütfen bakiye, gecikme ve proje sayıları için sayısal değer giriniz.")

def clear_form():
    entry_name.delete(0, tk.END)
    entry_company.delete(0, tk.END)
    entry_balance.delete(0, tk.END)
    entry_delay.delete(0, tk.END)
    entry_project.delete(0, tk.END)

def load_test():
    test_data = [
        ("Ali Yılmaz", "ABC A.Ş.", 10000, 5, 2),
        ("Veli Demir", "XYZ Ltd.", 30000, 20, 1),
        ("Ayşe Kaya", "QWE A.Ş.", 60000, 40, 0)
    ]
    for data in test_data:
        c = Customer(data[0], data[1], data[2], data[3], data[4])
        manager.add_customer(c)
    render_list()
    render_dashboard()

def render_list():
    listbox.delete(0, tk.END)
    for c in manager.get_all_customers():
        info = f"{c.name} - {c.company} | Bakiye: {c.balance} | Gecikme: {c.delay_days} | Risk: {c.risk_level}"
        if c.status_note:
            info += f" | Not: {c.status_note}"
        listbox.insert(tk.END, info)

def render_dashboard():
    data = manager.get_dashboard_data()
    dashboard_label.config(text=
        f"Toplam: {data['total']} | Yüksek Risk: {data['high']} | Orta: {data['medium']} | Düşük: {data['low']}\n"
        f"Ort Bakiye: {data['avg']:.2f} | Max Bakiye: {data['max_balance']} | Max Gecikme: {data['max_delay']}"
    )

# ------------------ UI (ARAYÜZ) ------------------
root = tk.Tk()
root.title("Müşteri Yönetim Paneli")
root.geometry("750x600")

# Form
tk.Label(root, text="Müşteri Giriş Formu", font=("Arial", 14, "bold")).pack(pady=10)
frame = tk.Frame(root)
frame.pack(pady=10)

labels = ["Müşteri Adı", "Firma Adı", "Açık Bakiye", "Gecikme Günü", "Aktif Proje"]
entries = []

for i, label_text in enumerate(labels):
    tk.Label(frame, text=label_text).grid(row=i, column=0, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

entry_name, entry_company, entry_balance, entry_delay, entry_project = entries

# Butonlar
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Müşteri Ekle", command=add_customer, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Temizle", command=clear_form, width=15).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Test Veri Yükle", command=load_test, bg="#2196F3", fg="white", width=15).grid(row=0, column=2, padx=10)

# Liste
tk.Label(root, text="Müşteri Listesi", font=("Arial", 12, "bold")).pack(pady=5)
listbox = tk.Listbox(root, width=90, height=10)
listbox.pack(pady=10)

# Dashboard
tk.Label(root, text="Dashboard", font=("Arial", 12, "bold")).pack(pady=5)
dashboard_label = tk.Label(root, text="", font=("Arial", 10), justify="center")
dashboard_label.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()
