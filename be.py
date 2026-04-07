
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

class Add:
    def __init__(self, customer):
        self.customer = customer

    def add_customer(self):
        # Müşteri ekleme işlemi burada yapılır
        print(f"{self.customer.name} adlı müşteri eklendi.")

class Service:
    def __init__(self, customer):
        self.customer = customer

    def provide_service(self):
        # Hizmet sağlama işlemi burada yapılır
        print(f"{self.customer.name} adlı müşteriye hizmet sağlanıyor.")

class Validate:
    def __init__(self, customer):
        self.customer = customer

        def validate_customer(self):
            # Müşteri doğrulama işlemi burada yapılır
            if self.customer.risk_level == "Yüksek Risk":
                print(f"{self.customer.name} adlı müşteri yüksek riskli olarak işaretlendi.")
            else:
                print(f"{self.customer.name} adlı müşteri doğrulandı.")

class İnput:
    def __init__(self, name, company, balance, delay_days, active_projects):
        self.name = name
        self.company = company
        self.balance = balance
        self.delay_days = delay_days
        self.active_projects = active_projects

    def get_customer_data(self):
        return Customer(self.name, self.company, self.balance, self.delay_days, self.active_projects)



