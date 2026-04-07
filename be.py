
class Customer:
    def __init__(self, name, company, balance, delay_days, active_projects):
        self.name = name
        self.company = company
        self.balance = float(balance)
        self.delay_days = int(delay_days)
        self.active_projects = int(active_projects)
        self.risk_level = "Normal"
        self.status_note = ""
        
        self.analyze_risk()

    def analyze_risk(self):
        notes = []
        
        if self.delay_days > 30:
            self.risk_level = "Yüksek Risk"
        elif self.delay_days > 20:
            self.risk_level = "Acil Uyarı"
        elif self.balance > 50000:
            self.risk_level = "Uyarı"

        if self.active_projects == 0:
            notes.append("Pasif Müşteri")
        if self.delay_days > 0:
            notes.append("Tahsilat Takibi")
            
        self.status_note = ", ".join(notes)







