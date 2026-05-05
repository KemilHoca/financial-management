import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from functools import partial

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
        
    def calculate_risk(self, balance: float, delay: int) -> str:
        """Risk hesaplama algoritması"""
        if balance > 50000 or delay > 30:
            return "High"
        elif balance > 20000 or delay > 15:
            return "Medium"
        return "Low"
    
    def validate(self, name: str, company: str, balance: float, 
                delay: int, project: int) -> Optional[str]:
        """Veri doğrulama"""
        if not name.strip():
            return "Müşteri adı boş olamaz"
        if not company.strip():
            return "Firma adı boş olamaz"
        if any(x < 0 for x in [balance, delay, project]):
            return "Negatif değer kullanılamaz"
        return None
    
    def get_form_data(self) -> Tuple[str, str, float, int, int]:
        """Form verilerini al"""
        return (
            self.entries[0].get().strip(),
            self.entries[1].get().strip(),
            float(self.entries[2].get()),
            int(self.entries[3].get()),
            int(self.entries[4].get())
        )
    
    def clear_form(self):
        """Formu temizle"""
        self.selected_index = None
        for entry in self.entries:
            entry.delete(0, tk.END)
    
    def refresh_all(self):
        """Tüm görünümleri yenile"""
        self.render_table()
        self.render_dashboard()

class CustomerUI:
    """Kullanıcı arayüzü sınıfı"""
    
    def __init__(self, manager: CustomerManager):
        self.manager = manager
        self.tree = None
        self.dashboard_var = tk.StringVar()
        self.setup_ui()
    
    def setup_ui(self):
        """Ana UI kurulumu"""
        self.root = tk.Tk()
        self.root.title("🏢 Müşteri Yönetim Sistemi PRO")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)
        
        # Modern stil
        style = ttk.Style()
        style.theme_use('clam')
        self.configure_styles()
        
        self.create_widgets()
        self.bind_events()
    
    def configure_styles(self):
        """Modern stil konfigürasyonu"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Dashboard.TLabel", font=("Segoe UI", 11))
        
        # Treeview stilleri
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        # Başlık
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10)
        ttk.Label(title_frame, text="🏢 Müşteri Yönetim Sistemi", 
                 style="Title.TLabel").pack()
        
        # Form paneli
        self.create_form_panel()
        
        # Buton paneli
        self.create_button_panel()
        
        # Tablo paneli
        self.create_table_panel()
        
        # Dashboard paneli
        self.create_dashboard_panel()
    
    def create_form_panel(self):
        """Form paneli oluştur"""
        form_frame = ttk.LabelFrame(self.root, text="📝 Yeni Müşteri Ekle/Düzenle", padding=15)
        form_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        labels = ["Müşteri Adı", "Firma Adı", "Açık Bakiye (₺)", "Gecikme (Gün)", "Aktif Proje"]
        
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text, font=("Segoe UI", 10)).grid(
                row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=5)
            
            entry = ttk.Entry(form_frame, font=("Segoe UI", 10), width=20)
            entry.grid(row=i//2, column=(i%2)*2+1, sticky="ew", padx=5, pady=5)
            self.manager.entries.append(entry)
        
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
    
    def create_button_panel(self):
        """Buton paneli oluştur"""
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        buttons = [
            ("➕ Ekle", self.manager.add_customer),
            ("✏️ Güncelle", self.manager.update_customer),
            ("🗑️ Sil", self.manager.delete_customer),
            ("🔄 Temizle", self.manager.clear_form),
            ("📊 Test Veri", self.manager.load_test_data)
        ]
        
        for i, (text, command) in enumerate(buttons):
            ttk.Button(btn_frame, text=text, command=command, 
                      style="Accent.TButton").grid(row=0, column=i, padx=8)
    
    def create_table_panel(self):
        """Tablo paneli oluştur"""
        table_frame = ttk.LabelFrame(self.root, text="📋 Müşteri Listesi", padding=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Scrollbar'lı Treeview
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_frame, show="headings", height=12)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Sütunlar
        columns = ("id", "name", "company", "balance", "delay", "risk")
        headers = ("ID", "Müşteri", "Firma", "Bakiye", "Gecikme", "Risk")
        
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=120 if col != "name" else 150)
        
        # Risk renkleri
        self.tree.tag_configure("High", background="#ffebee", foreground="#c62828")
        self.tree.tag_configure("Medium", background="#fff3e0", foreground="#ef6c00")
        self.tree.tag_configure("Low", background="#e8f5e8", foreground="#2e7d32")
    
    def create_dashboard_panel(self):
        """Dashboard paneli oluştur"""
        dash_frame = ttk.LabelFrame(self.root, text="📈 İstatistikler", padding=15)
        dash_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(dash_frame, textvariable=self.dashboard_var, 
                 style="Dashboard.TLabel").pack()
    
    def bind_events(self):
        """Event'leri bağla"""
        self.tree.bind("<<TreeviewSelect>>", self.on_customer_select)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_customer_select(self, event):
        """Müşteri seçimi"""
        self.manager.select_customer(event)
    
    def on_closing(self):
        """Uygulama kapanırken"""
        self.root.destroy()
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

# Manager metodları (CustomerManager sınıfına eklenecek)
def add_customer(self):
    try:
        name, company, balance, delay, project = self.get_form_data()
        
        error = self.validate(name, company, balance, delay, project)
        if error:
            messagebox.showerror("❌ Hata", error, parent=self.ui.root)
            return
        
        risk = self.calculate_risk(balance, delay)
        
        customer = Customer(name, company, balance, delay, project, risk)
        self.customers.append(customer)
        
        self.refresh_all()
        self.clear_form()
        messagebox.showinfo("✅ Başarılı", "Müşteri başarıyla eklendi!")
        
    except ValueError:
        messagebox.showerror("❌ Hata", "Lütfen sayısal alanlara geçerli sayı girin!")
    except Exception as e:
        messagebox.showerror("❌ Hata", f"Beklenmeyen hata: {str(e)}")

def update_customer(self):
    if self.selected_index is None:
        messagebox.showerror("❌ Hata", "Lütfen düzenlenecek kaydı seçin!")
        return
    
    try:
        name, company, balance, delay, project = self.get_form_data()
        
        error = self.validate(name, company, balance, delay, project)
        if error:
            messagebox.showerror("❌ Hata", error, parent=self.ui.root)
            return
        
        risk = self.calculate_risk(balance, delay)
        self.customers[self.selected_index] = Customer(
            name, company, balance, delay, project, risk
        )
        
        self.refresh_all()
        self.clear_form()
        messagebox.showinfo("✅ Başarılı", "Müşteri başarıyla güncellendi!")
        
    except Exception as e:
        messagebox.showerror("❌ Hata", f"Güncelleme hatası: {str(e)}")

def delete_customer(self):
    if self.selected_index is None:
        messagebox.showerror("❌ Hata", "Lütfen silinecek kaydı seçin!")
        return
    
    name = self.customers[self.selected_index].name
    if messagebox.askyesno("🗑️ Silme Onayı", 
                          f"'{name}' müşterisi silinecek.\nOnaylıyor musunuz?"):
        del self.customers[self.selected_index]
        self.selected_index = None
        self.refresh_all()
        messagebox.showinfo("✅ Silindi", "Müşteri başarıyla silindi!")

def select_customer(self, event):
    selected = self.tree.focus()
    if not selected:
        return
    
    values = self.tree.item(selected, "values")
    self.selected_index = int(values[0])
    
    customer = self.customers[self.selected_index]
    
    self.entries[0].delete(0, tk.END)
    self.entries[1].delete(0, tk.END)
    self.entries[2].delete(0, tk.END)
    self.entries[3].delete(0, tk.END)
    self.entries[4].delete(0, tk.END)
    
    self.entries[0].insert(0, customer.name)
    self.entries[1].insert(0, customer.company)
    self.entries[2].insert(0, str(customer.balance))
    self.entries[3].insert(0, str(customer.delay))
    self.entries[4].insert(0, str(customer.project))

def render_table(self):
    for item in self.tree.get_children():
        self.tree.delete(item)
    
    for i, customer in enumerate(self.customers):
        self.tree.insert("", "end", values=(
            i, customer.name, customer.company, 
            f"{customer.balance:,.0f}", customer.delay, customer.risk
        ), tags=(customer.risk,))

def render_dashboard(self):
    if not self.customers:
        self.dashboard_var.set("📊 Veri yok - Lütfen müşteri ekleyin")
        return
    
    total = len(self.customers)
    risks = {"High": 0, "Medium": 0, "Low": 0}
    total_balance = sum(c.balance for c in self.customers)
    max_balance = max(c.balance for c in self.customers)
    max_delay = max(c.delay for c in self.customers)
    
    for c in self.customers:
        risks[c.risk] += 1
    
    avg_balance = total_balance / total
    
    self.dashboard_var.set(
        f"👥 Toplam: {total} | "
        f"🔴 Yüksek: {risks['High']} | "
        f"🟡 Orta: {risks['Medium']} | "
        f"🟢 Düşük: {risks['Low']} | "
        f"💰 Ortalama: {avg_balance:,.0f}₺ | "
        f"📈 Max Bakiye: {max_balance:,.0f}₺ | "
        f"⏰ Max Gecikme: {max_delay} gün"
    )

def load_test_data(self):
    """Test verilerini yükle"""
    test_data = [
        ("Ahmet Yılmaz", "TechCorp", 15000, 8, 2),
        ("Ayşe Kaya", "Finans Ltd", 45000, 25, 1),
        ("Mehmet Demir", "ProjeCo", 75000, 45, 4),
        ("Fatma Şahin", "StartupX", 12000, 3, 3),
        ("Ali Çelik", "Endüstri A.Ş.", 28000, 18, 2)
    ]
    
    self.customers.clear()
    for name, company, balance, delay, project in test_data:
        risk = self.calculate_risk(balance, delay)
        self.customers.append(Customer(name, company, balance, delay, project, risk))
    
    self.refresh_all()
    messagebox.showinfo("✅ Test Verisi", "5 örnek müşteri yüklendi!")

# Manager metodlarına bağla
CustomerManager.add_customer = add_customer
CustomerManager.update_customer = update_customer
CustomerManager.delete_customer = delete_customer
CustomerManager.select_customer = select_customer
CustomerManager.render_table = render_table
CustomerManager.render_dashboard = render_dashboard
CustomerManager.load_test_data = load_test_data
CustomerManager.refresh_all = refresh_all
CustomerManager.clear_form = clear_form
CustomerManager.get_form_data = get_form_data
CustomerManager.validate = validate
CustomerManager.calculate_risk = calculate_risk

# Uygulamayı başlat
if __name__ == "__main__":
    manager = CustomerManager()
    ui = CustomerUI(manager)
    manager.ui = ui  # UI referansını manager'a ver
    ui.run()
