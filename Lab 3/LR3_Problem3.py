class SavingsAccount:
    
    def __init__(self, name, pin, balance=0.0):
        self.name = name
        self.pin = pin
        self.balance = balance
    
    def __str__(self):
        return f"Name: {self.name}\nPIN: {self.pin}\nBalance: ${self.balance:.2f}"
    
    def getName(self):
        return self.name
    
    def getPin(self):
        return self.pin
    
    def getBalance(self):
        return self.balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"${amount:.2f} deposited"
        else:
            return "Invalid deposit amount"
    
    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"${amount:.2f} withdrawn"
        else:
            return "Invalid withdrawal amount or insufficient funds"
    
    def computeInterest(self):
        interest = self.balance * 0.02
        return interest
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __ge__(self, other):
        return self.name >= other.name

import pickle
import random

class Bank:
    def __init__(self, fileName = None):
        self.accounts = {}
        self.fileName = fileName
        if fileName != None:
            fileObj = open(fileName, 'rb')
            while True:
                try:
                    account = pickle.load(fileObj)
                    self.add(account)
                except Exception:
                    fileObj.close()
                    break

    def __str__(self):
        sorted_accounts = sorted(self.accounts.values(), key=lambda account: account.getName())
        return "\n".join(map(str, sorted_accounts))

    def makeKey(self, name, pin):
        return name + "/" + pin

    def add(self, account):
        key = self.makeKey(account.getName(), account.getPin())
        self.accounts[key] = account

    def remove(self, name, pin):
        key = self.makeKey(name, pin)
        return self.accounts.pop(key, None)

    def get(self, name, pin):
        key = self.makeKey(name, pin)
        return self.accounts.get(key, None)

    def computeInterest(self):
        total = 0
        for account in self.accounts.values():  # Fixed: was self._accounts
            total += account.computeInterest()
        return total

    def getKeys(self):
        return sorted(self.accounts.keys())

    def save(self, fileName = None):
        if fileName != None:
            self.fileName = fileName
        elif self.fileName == None:
            return
        fileObj = open(self.fileName, 'wb')
        for account in self.accounts.values():
            pickle.dump(account, fileObj)
        fileObj.close()

def createBank(numAccounts = 1):
    names = ("Brandon", "Molly", "Elena", "Mark", "Tricia",
             "Ken", "Jill", "Jack")
    bank = Bank()
    upperPin = numAccounts + 1000
    for pinNumber in range(1000, upperPin):
        name = random.choice(names)
        balance = float(random.randint(100, 1000))
        bank.add(SavingsAccount(name, str(pinNumber), balance))
    return bank

def testAccount():
    account = SavingsAccount("Ken", "1000", 500.00)
    print(account)
    print(account.deposit(100))
    print("Expect 600:", account.getBalance())
    print(account.deposit(-50))
    print("Expect 600:", account.getBalance())
    print(account.withdraw(100))
    print("Expect 500:", account.getBalance())
    print(account.withdraw(-50))
    print("Expect 500:", account.getBalance())
    print(account.withdraw(100000))
    print("Expect 500:", account.getBalance())

def main(number = 10, fileName = None):
    testAccount()
    print("\n" + "="*50)
    print("BANK ACCOUNTS (sorted by name):")
    print("="*50)
    
    if fileName:
        bank = Bank(fileName)
    else:
        bank = createBank(number)
    print(bank)
    
    print("\n" + "="*30)
    print("SORTED KEYS:")
    print("="*30)
    for key in bank.getKeys():
        print(key)
    
    print(f"\nTotal interest on all accounts: ${bank.computeInterest():.2f}")

if __name__ == "__main__":
    main()