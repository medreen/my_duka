class BankAccount:
    def __init__(self, account_no, name, balance, date_opened):
        self.account_number = account_no
        self.owner_name = name
        self.balance = balance
        self.date_opened = date_opened

    def deposit(self, amount):
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        self.balance -= amount
        return self.balance
    
    def display_info(self):
        return f"------USER INFO------ \nAccount number: {self.account_number} \nUser name: {self.owner_name} \nBalance: {self.balance} \nDate of registeration: {self.date_opened}."
    
user_1 = BankAccount(1, "Lucas", 300, "1-Jan")
print(user_1)

dep = user_1.deposit(200)
print(dep)

wtd = user_1.withdraw(50)
print(wtd)

info = user_1.display_info()
print(info)