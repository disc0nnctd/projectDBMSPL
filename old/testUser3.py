from tkinter import *
from pymongo import MongoClient

constring='mongodb+srv://disc0nnctd:dc123@disc0nnctd-e3fyk.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(constring)
db=client.users
res="300x400"

window=Tk()
window.geometry(res)
window.resizable(width=False, height=False)
window.title("notUber")
ff=Frame(window)

class UserLogin:
    #---MessageLabels----
    cannotbeempty=Label(ff, text="Fields cannot be empty!")
    authenticatedstring=Label(ff, text="Authenticated!")
    invaliduserpass=Label(ff, text="Invalid Username/Password pair. Try again.")
    pleaseregister=Label(ff, text="Please register.")
    alreadyexists=Label(ff, text="User already exists!")
    registeredyay=Label(ff, text="Registered! Try logging in!")
    #-------------
    def __init__(self):
        self.user=StringVar()
        self.pwd=StringVar()
        self.authsuccess=False

    def forgetmessages():
        UserLogin.cannotbeempty.grid_forget()
        UserLogin.authenticatedstring.grid_forget()
        UserLogin.invaliduserpass.grid_forget()
        UserLogin.pleaseregister.grid_forget()
        UserLogin.alreadyexists.grid_forget()
        UserLogin.registeredyay.grid_forget()
    def login(self):
        UserLogin.forgetmessages()
        uname=self.user.get()
        pd=self.pwd.get()
        if(uname and pd):
            dt = db.user.find_one({'_id': uname})
            if(dt):
                if dt['password']==pd:
                    UserLogin.authenticatedstring.grid()
                    #next window
                    self.authsuccess=True
                    self.suicide()
                else:
                    UserLogin.invaliduserpass.grid()
            else:
                UserLogin.pleaseregister.grid()
        else:
            UserLogin.cannotbeempty.grid()
    def register(self):
        UserLogin.forgetmessages()
        uname=self.user.get()
        pd=self.pwd.get()
        if uname:
            dt = db.user.find_one({'_id': uname})
            if(dt):
                UserLogin.alreadyexists.grid()
            else:
                db.user.insert_one({'_id':uname, 'password':pd})
                UserLogin.registeredyay.grid()
        else:
            UserLogin.cannotbeempty.grid()
    def generate(self): 
        Label(ff, text="Login/Register", bg="gray", width="30", height="2", font=("Calibri", 14)).grid()
        Label(ff, text="Username", font=("Calibri", 12)).grid(pady=10)
        Entry(ff, textvariable=self.user).grid(pady=2) #username
        Label(ff, text="Password", font=("Calibri", 12)).grid(pady=5)
        Entry(ff, textvariable=self.pwd).grid(pady=2) #password
        Button(ff, text="Login", height="2", width="10", command=self.login).grid(pady=10)
        Button(ff, text="Register", height="2", width="10", command=self.register).grid(pady=10)
        ff.grid()
    def suicide(self):
        ff.grid_forget()

class UserPage:
    def __init__(self, username):
        Label(ff, text=("Welcome %d!"%username), bg="gray", width="30", height="2", font=("Calibri", 14)).grid()
        
a=UserLogin()
a.generate()
