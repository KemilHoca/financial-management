# be.py
# Git Branch: backend-dev (veya benzeri)

class Customer:
    def __init__(self, name, company, balance, delay_days, active_projects):
        self.name = name
        self.company = company
        self.balance = float(balance)
        self.delay_days = int(delay_days)
        self.active_projects = int(active_projects)
        self.risk_level = ""
        self.status_note = ""
        
        self.analyze_risk()

    def analyze_risk(self):
        if self.balance > 50000 or self.delay_days > 30:
            self.risk_level = "High"
        elif self.balance > 20000 or self.delay_days > 15:
            self.risk_level = "Medium"
        else:
            self.risk_level = "Low"

        notes = []
        if self.active_projects == 0:
            notes.append("Pasif Müşteri")
        if self.delay_days > 0:
            notes.append("Tahsilat Takibi")
            
        self.status_note = ", ".join(notes)

class CustomerManager:
    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def get_all_customers(self):
        return self.customers

    def get_dashboard_data(self):
        total = len(self.customers)
        high = medium = low = 0
        total_balance = max_balance = max_delay = 0

        for c in self.customers:
            if c.risk_level == "High":
                high += 1
            elif c.risk_level == "Medium":
                medium += 1
            else:
                low += 1

            total_balance += c.balance
            if c.balance > max_balance:
                max_balance = c.balance
            if c.delay_days > max_delay:
                max_delay = c.delay_days

        avg = total_balance / total if total > 0 else 0

        return {
            "total": total,
            "high": high,
            "medium": medium,
            "low": low,
            "avg": avg,
            "max_balance": max_balance,
            "max_delay": max_delay
        }

# Dosya direkt çalıştırılırsa bu kısım devreye girer (Backend testi için)
if __name__ == "__main__":
    print("Backend servisi aktif. Modül olarak içe aktarılmaya (import) hazır.")
