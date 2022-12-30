from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
import sqlite3
from Jrgeter_BankAccount import BankAccount
conn = None
cursor = None

conn = sqlite3.connect('Userlog.db')

cursor = conn.cursor()
command1 = cursor.execute("""CREATE TABLE IF NOT EXISTS users(
  firstName TEXT,
  lastName TEXT,
  username TEXT PRIMARY KEY,
  password TEXT,
  balance REAL, 
  tranaction TEXT)""")

conn.commit()

class App:
    def __init__(self, root):
        self.root = root
        self.userimgFile = Image.open("imgs/userImg.png")
        self.userimgFile= self.userimgFile.resize((100,100))
        self.userimg = ImageTk.PhotoImage(self.userimgFile)

        self.label = Label(self.root, text="User Login", font=("Calibri", 20), image=self.userimg)
        self.label.pack(pady=20)

        self.subimgfile = Image.open("imgs/loginimgg.png")
        self.subimgfile = self.subimgfile.resize((35,35))
        self.submimg = ImageTk.PhotoImage(self.subimgfile)

        self.userNameLabel = Label(self.root, text="Enter username", font=("Calibri", 11)).pack(pady=5)
        self.userNameEntry = ttk.Entry(root, width=40)
        self.userNameEntry.pack()

        self.passwordLabel = Label(self.root, text="Enter password", font=("Calibri", 11)).pack(pady=5)
        self.passwordEntry = ttk.Entry(root, width=40)
        self.passwordEntry.pack()

        style = ttk.Style()
        style.configure('TButton', font=("Calibri", 9))
        self.entertBtn = ttk.Button(self.root, text="Enter", image=self.submimg, command=partial(App.enter, self)) #FIXME add command to open content window
        self.entertBtn.place(x=320, y=195)

        self.newUserBtn = ttk.Button(self.root, text="Don't have an account? Create one", command=App.createNewUser) 
        self.newUserBtn.pack(pady=25)
        
        
    def enter(self):
        username = self.userNameEntry.get()
        password = self.passwordEntry.get()    
        
        myList = [username, password]
        
        conn = None
        c = None         
        conn = sqlite3.connect("userLog.db")
        c = conn.cursor()
        
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (myList))
        result = c.fetchone()
        conn.commit()
        conn.close()
        print(result)
        
        if result:
            newWin = ThirdWin(username, password)
            
        self.userNameEntry.delete(0, END)
        self.passwordEntry.delete(0, END)
        
    def createNewUser():
        secWin = SecondWindow()
        
class SecondWindow(tk.Toplevel, App):
    def __init__(self):
        self.secWin = Toplevel()
        self.secWin.title("New User")
        self.secWin.geometry("375x400")  
    
        self.label = ttk.Label(self.secWin, text="Create New Account", font=("Calibri", 18)).pack(pady=20)
        
        self.fnText = tk.StringVar()
        self.fnText.set("First Name")
        self.fnameLabel = ttk.Label(self.secWin, text="First Name", font=("Calibri", 11)).pack(pady=5)
        self.fnameEntry = ttk.Entry(self.secWin, width=20)
        self.fnameEntry.pack()
        
        
        self.lnameLabel = ttk.Label(self.secWin, text="Last Name", font=("Calibri", 11)).pack(pady=5)
        self.lnameEntry = ttk.Entry(self.secWin, width=20)
        self.lnameEntry.pack()
        
        self.newUserLabel = ttk.Label(self.secWin, text="Create username", font=("Calibri", 11)).pack(pady=5)
        self.newUserEntry = ttk.Entry(self.secWin, width=20)
        self.newUserEntry.pack()

        self.newPasswordLabel = Label(self.secWin, text="Create password", font=("Calibri", 11)).pack(pady=5)
        self.newPasswordEntry = ttk.Entry(self.secWin, width=20)
        self.newPasswordEntry.pack()

        style = ttk.Style()
        style.configure("TButton", font=("Calibri", 9))
        self.submitBtn = ttk.Button(self.secWin, text="Create Account", command=partial(SecondWindow.databaseEntry, self, self.newUserEntry, self.newPasswordEntry))
        self.submitBtn.pack(pady=10)
        
        self.backBtn = ttk.Button(self.secWin, text="Back to sign in", command=SecondWindow.backHome)
        self.backBtn.pack(pady=8)
        
    
    def databaseEntry(self, username, password):
        userInfo = [str(self.fnameEntry.get()), str(self.lnameEntry.get()), str(self.newUserEntry.get()), str(self.newPasswordEntry.get())]
        conn = None
        c = None
                    
        conn = sqlite3.connect("userLog.db")
        c = conn.cursor()
        c.execute("INSERT INTO users(firstName, lastName, username, password) VALUES(?,?,?,?)", (userInfo))
                             
        conn.commit()
        conn.close()
        print("It worked", str(self.newUserEntry.get()), str(self.newPasswordEntry.get()))
        self.newUserEntry.delete(0, END)
        self.newPasswordEntry.delete(0, END)
        
    def backHome():
        for widget in root.winfo_children():
            if "toplevel" in str(widget):
                widget.destroy()
                
class ThirdWin(tk.Toplevel, App, BankAccount):
    def __init__(self, username, password):
        self.userNameEntry = username
        self.passwordEntry = password
        
        self.thirdWin = Toplevel()
        self.thirdWin.title("QBank")
        self.thirdWin.geometry("375x400")
        
        self.label = Label(self.thirdWin, text="Welcome " + str(self.userNameEntry), font=("Calibri", 18))
        self.label.pack(pady=32)
        style = ttk.Style()
        style.configure("TButton", font=("Calibri", 9))
        self.logoutBtn = ttk.Button(self.thirdWin, text="Logout", command=partial(ThirdWin.logout, self)) 
        self.logoutBtn.place(x=290, y=5)
        self.homeBtn = ttk.Button(self.thirdWin, text="Home", command=partial(ThirdWin.goHome, self))
        self.homeBtn.place(x=10, y=5)
        
        self.userList = [self.userNameEntry, self.passwordEntry]
        
        self.conn = sqlite3.connect('UserLog.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT balance FROM users WHERE username = ? AND password = ?", (self.userList))
        self.bal = self.cursor.fetchone()
        print(self.bal)
        self.conn.commit()
        self.conn.close()
        
        
        self.bank = BankAccount()
        if self.bal[0] == None:
            self.bank.setBalance(balance=0)
            
            self.balLabel = Label(self.thirdWin, text="Your current balance is: $0.00.")
        else:
            self.bank.setBalance(balance=self.bal[0])    
            self.balLabel = Label(self.thirdWin, text="Your current balance is: $" + str(self.bal[0]) + ".")
        self.balLabel.pack()
        self.btnFrame = ThirdWin.gridFrame(self)
        
    def gridFrame(self):
        self.frame = Frame(self.thirdWin)   
        self.frame.pack(padx=5, pady=50)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(4, weight=1)
        
        self.depositBtn = ttk.Button(self.frame, text="Deposit", command=partial(ThirdWin.depositFrame, self))
        self.depositBtn.grid(column=0, row=2, padx= 7, sticky="news")
        self.withBtn = ttk.Button(self.frame, text="Withdraw", command=partial(ThirdWin.withFrame, self))
        self.withBtn.grid(column=1, row=2, padx=7, sticky="news", rowspan=2)
        self.prevTrans = ttk.Button(self.frame, text="View Previous Transactions", command=partial(ThirdWin.prevTransBtn, self))
        self.prevTrans.grid(column=0, row=4, pady=14, padx=7, columnspan= 2, sticky='news')
        
                    
    def logout(self):
        for self.widget in self.thirdWin.winfo_children():
            self.widget.destroy() 
        self.goodBye = Label(self.thirdWin, text="Good Bye!", font=("Calibri", 18))
        self.goodBye.pack(pady=30)
        self.logoutMsg = Label(self.thirdWin, text=f"Succesfully Logged Out. \n Thank you for using QBank", font=("Calibri", 15))
        self.logoutMsg.pack(pady=15)
        
        
        
        # tester code
        conn = sqlite3.connect('UserLog.db')
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE username = ? AND password = ?", (self.userList))
        self.bal = cursor.fetchone()
        print(self.bal)
        conn.commit()
        conn.close()
        
        self.dbBalance = float(self.bank.getBalance())
        userInfo = [self.dbBalance, str(self.userNameEntry), str(self.passwordEntry)]
        print(userInfo)
        conn = sqlite3.connect('UserLog.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE username = ? AND password = ?", (userInfo))
        conn.commit()
        conn.close()
        
        print("Balance added")
        
        
    def goHome(self):      #FIXME: redo code to display balance 
        for widget in self.thirdWin.winfo_children():
           widget.place_forget()
        
        self.label = Label(self.thirdWin, text="Welcome " + str(self.userNameEntry), font=("Calibri", 18))
        self.label.pack(pady=32)
        style = ttk.Style()
        style.configure("TButton", font=("Calibri", 9))
        self.logoutBtn = ttk.Button(self.thirdWin, text="Logout", command=partial(ThirdWin.logout, self)) 
        self.logoutBtn.place(x=290, y=5)
        self.homeBtn = ttk.Button(self.thirdWin, text="Home", command=partial(ThirdWin.goHome, self))
        self.homeBtn.place(x=10, y= 5)
        self.balLabel = Label(self.thirdWin, text="Your current balance is: $" + str(self.bank.getBalance()) + ".")
        self.balLabel.pack()
        self.btnFrame = ThirdWin.gridFrame(self) 

    def depositFrame(self):
        for widget in self.thirdWin.winfo_children():
            widget.forget()
        
        self.depLabel = Label(self.thirdWin, text="Enter Amount to Deposit:", font=("Calibri", 18))
        self.depLabel.place(x=65, y=100)
        self.depEntry = ttk.Entry(self.thirdWin, width=15)
        self.depEntry.place(x=140, y=150)
        self.depBtn = ttk.Button(self.thirdWin, text="Enter", command=partial(ThirdWin.subDeposit, self))
        self.depBtn.place(x=150, y=200)
        
    def subDeposit(self):
        self.bank.deposit(float(self.depEntry.get()))
        print(self.bank.getPreviousTransaction())
        print(f'Balance ${self.bank.getBalance()}')
        userMsg = Label(self.thirdWin, text=str(self.bank.getPreviousTransaction()), font=("Calibri", 11))
        userMsg.place(x=125, y=250)
        self.depEntry.delete(0, END)
        
    def withFrame(self):
        for widget in self.thirdWin.winfo_children():
            widget.forget()
        
        self.withLabel = Label(self.thirdWin, text="Enter Amount to Withdraw:", font=("Calibri", 18))
        self.withLabel.place(x=65, y=100)
        self.withEntry = ttk.Entry(self.thirdWin, width=15)
        self.withEntry.place(x=140, y=150)
        self.withBtn = ttk.Button(self.thirdWin, text="Enter", command=partial(ThirdWin.subWith, self))
        self.withBtn.place(x=150, y=200)
        
    def subWith(self):
        self.bank.withdraw(float(self.withEntry.get()))
        print(self.bank.getPreviousTransaction())
        print(f'Balance ${self.bank.getBalance()}')
        userMsg = Label(self.thirdWin, text=str(self.bank.getPreviousTransaction()), font=("Calibri", 11))
        userMsg.place(x=125, y=250)
        self.withEntry.delete(0, END)
        
        
    def prevTransBtn(self):
        print("FIXME")
        
   
def main():
    global root
    root = Tk()
    root.title("Login")
    root.geometry("375x400")
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
