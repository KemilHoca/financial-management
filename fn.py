import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Customer:
    """Müşteri veri modeli"""
    name: str
    company: str
    balance: float
    delay: int
    project: int
    risk: str = ""

class CustomerManager:
    """Ana müşteri yönetim sınıfı"""
    
    def __init__(self):
        self.customers: List[Customer] = []
        self.selected_index: Optional[int] = None
        self.entries = []
        self.ui = None 
        
    def calculate_risk(self, balance: float, delay: int) -> str:
        if balance > 50000 or delay > 30:
            return "High"
        elif balance > 20000 or delay > 15:
            return "Medium"
        return "Low"
    
    def validate(self, name: str, company: str, balance: float, 
                delay: int, project: int) -> Optional[str]:
        if not name.strip():
            return "Müşteri adı boş olamaz"
        if not company.strip():
            return "Firma adı boş olamaz"
        if any(x < 0 for x in [balance, delay, project]):
            return "Negatif değer kullanılamaz"
        return None
    
    def get_form_data(self) -> Tuple[str, str, float, int, int]:
        return (
            self.entries[0].get().strip(),
            self.entries[1].get().strip(),
            float(self.entries[2].get() or 0),
            int(self.entries[3].get() or 0),
            int(self.entries[4].get() or 0)
        )
    
    def clear_form(self):
        self.selected_index = None
        for entry in self.entries:
            entry.delete(0, tk.END)
    
    def refresh_all(self):
        self.render_table()
        self.render_dashboard()

    def add_customer(self):
        try:
            name, company, balance, delay, project = self.get_form_data()
            error = self.validate(name, company, balance, delay, project)
            if error:
                messagebox.showerror("❌ Hata", error)
                return
            
            risk = self.calculate_risk(balance, delay)
            self.customers.append(Customer(name, company, balance, delay, project, risk))
            self.refresh_all()
            self.clear_form()
            messagebox.showinfo("✅ Başarılı", "Müşteri başarıyla eklendi!")
        except ValueError:
            messagebox.showerror("❌ Hata", "Lütfen sayısal alanlara geçerli sayı girin!")

    def update_customer(self):
        if self.selected_index is None:
            messagebox.showerror("❌ Hata", "Lütfen düzenlenecek kaydı seçin!")
            return
        try:
            name, company, balance, delay, project = self.get_form_data()
            risk = self.calculate_risk(balance, delay)
            self.customers[self.selected_index] = Customer(name, company, balance, delay, project, risk)
            self.refresh_all()
            self.clear_form()
            messagebox.showinfo("✅ Başarılı", "Müşteri güncellendi!")
        except Exception as e:
            messagebox.showerror("❌ Hata", f"Hata: {str(e)}")

    def delete_customer(self):
        if self.selected_index is None:
            messagebox.showerror("❌ Hata", "Lütfen silinecek kaydı seçin!")
            return
        if messagebox.askyesno("🗑️ Sil", "Bu kaydı silmek istediğinize emin misiniz?"):
            del self.customers[self.selected_index]
            self.selected_index = None
            self.refresh_all()
            self.clear_form()

    def select_customer(self, event):
        selected = self.ui.tree.focus()
        if not selected: return
        values = self.ui.tree.item(selected, "values")
        if not values: return
            
        self.selected_index = int(values[0])
        customer = self.customers[self.selected_index]
        
        for entry in self.entries: entry.delete(0, tk.END)
        self.entries[0].insert(0, customer.name)
        self.entries[1].insert(0, customer.company)
        self.entries[2].insert(0, str(customer.balance))
        self.entries[3].insert(0, str(customer.delay))
        self.entries[4].insert(0, str(customer.project))

    def render_table(self):
        for item in self.ui.tree.get_children(): self.ui.tree.delete(item)
        for i, c in enumerate(self.customers):
            self.ui.tree.insert("", "end", values=(i, c.name, c.company, f"{c.balance:,.0f}", c.delay, c.risk), tags=(c.risk,))

    def render_dashboard(self):
        if not self.customers:
            self.ui.dashboard_var.set("📊 Veri yok")
            return
        total = len(self.customers)
        total_balance = sum(c.balance for c in self.customers)
        self.ui.dashboard_var.set(f"👥 Toplam Müşteri: {total} | 💰 Toplam Bakiye: {total_balance:,.0f} ₺")

    def load_test_data(self):
        test_data = [("Ahmet Yılmaz", "TechCorp", 15000, 8, 2), ("Ayşe Kaya", "Finans Ltd", 45000, 25, 1)]
        for name, company, balance, delay, project in test_data:
            risk = self.calculate_risk(balance, delay)
            self.customers.append(Customer(name, company, balance, delay, project, risk))
        self.refresh_all()

class CustomerUI:
    def __init__(self, manager: CustomerManager):
        self.manager = manager
        self.setup_ui()
    
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("🏢 Müşteri Yönetim Sistemi PRO")
        self.root.geometry("1000x700")
        self.dashboard_var = tk.StringVar(value="📊 Veri yok")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Üst Panel
        header = ttk.Frame(self.root)
        header.pack(pady=10)
        ttk.Label(header, text="Müşteri Yönetim Paneli", font=("Segoe UI", 14, "bold")).pack()

        # Form
        self.create_form_panel()
        
        # Butonlar
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="➕ Ekle", command=self.manager.add_customer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✏️ Güncelle", command=self.manager.update_customer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Sil", command=self.manager.delete_customer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📊 Test Veri", command=self.manager.load_test_data).pack(side="left", padx=5)

        # Tablo
        self.create_table_panel()
        
        # İstatistik
        ttk.Label(self.root, textvariable=self.dashboard_var, font=("Segoe UI", 10, "italic")).pack(pady=10)

    def create_form_panel(self):
        frame = ttk.LabelFrame(self.root, text="Müşteri Bilgileri", padding=10)
        frame.pack(fill="x", padx=20)
        labels = ["Müşteri", "Firma", "Bakiye", "Gecikme", "Proje"]
        for i, text in enumerate(labels):
            ttk.Label(frame, text=text).grid(row=0, column=i*2, padx=5)
            ent = ttk.Entry(frame, width=15)
            ent.grid(row=0, column=i*2+1, padx=5)
            self.manager.entries.append(ent)

    def create_table_panel(self):
        columns = ("id", "name", "company", "balance", "delay", "risk")
        # HATANIN DÜZELTİLDİĞİ YER: columns parametresi eklendi
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        
        headers = ["ID", "Müşteri", "Firma", "Bakiye", "Gecikme", "Risk"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=100, anchor="center")
            
        self.tree.pack(fill="both", expand=True, padx=20)
        self.tree.bind("<<TreeviewSelect>>", self.manager.select_customer)
        
        self.tree.tag_configure("High", background="#ffcccc")
        self.tree.tag_configure("Medium", background="#ffffcc")
        self.tree.tag_configure("Low", background="#ccffcc")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    manager = CustomerManager()
    ui = CustomerUI(manager)
    manager.ui = ui
    ui.run()
