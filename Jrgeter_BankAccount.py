#  John Geter
#  COMP-163 : Section 001
#  Derrick Leflore
#  BankAccount is a class used to represent a running total of a user’s bank balance and
#  allows the user to perform various actions.
import string

class BankAccount:
    balance: int
    customerName: string 
    customerId: int
    previousTransaction: int
    
    def __init__(self, CustomerName='ABC', CustomerID=0): # instance variables
        self.balance = 0
        self.customerId = CustomerID
        self.customerName = CustomerName
        self.previousTransaction = "No transaction has occured"
    
    # Defining methods for BankAccount class
    def getBalance(self):
        return (f'{self.balance:.2f}')
    
    def setBalance(self, balance=0):
        self.balance = balance 
        
    def getCustomerId(self):
        return self.customerId
    
    def setCustomerId(self, customerId=0):
        self.customerId = customerId
    
    def getCustomerName(self):
        return self.customerName
    
    def setCustomerName(self, name):
        self.customerName = name
        
    def getPreviousTransaction(self):
        return self.previousTransaction
    
    def setPreviousTransaction(self, previousTransaction):
        self.previousTransaction = previousTransaction

    def withdraw(self, amount):
        self.previousTransaction = f'Withdrawn: ${amount:.2f}'
        self.balance -= amount
        
    
    def deposit(self, amount):
        self.previousTransaction = f'Deposited: ${amount:.2f}'
        self.balance += amount
        
    def __str__(self):
        return (f'{self.getBalance()}')

