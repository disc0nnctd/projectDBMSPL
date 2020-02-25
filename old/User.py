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


user=StringVar()
pwd=StringVar()

#---MessageLabels----
cannotbeempty=Label(ff, text="Fields cannot be empty!")
authenticatedstring=Label(ff, text="Authenticated!")
invaliduserpass=Label(ff, text="Invalid Username/Password pair. Try again.")
pleaseregister=Label(ff, text="Please register.")
alreadyexists=Label(ff, text="User already exists!")
registeredyay=Label(ff, text="Registered! Try logging in!")
#-------------

def forgetmessages():
    cannotbeempty.grid_forget()
    authenticatedstring.grid_forget()
    invaliduserpass.grid_forget()
    pleaseregister.grid_forget()
    alreadyexists.grid_forget()
    registeredyay.grid_forget()
def login():
    forgetmessages()
    uname=user.get()
    pd=pwd.get()
    if(uname and pd):
        dt = db.user.find_one({'_id': uname})
        if(dt):
            if dt['password']==pd:
                authenticatedstring.grid()
                #next window
            else:
                invaliduserpass.grid()
        else:
            pleaseregister.grid()
    else:
        cannotbeempty.grid()
    
        
def register():
    forgetmessages()
    uname=user.get()
    pd=pwd.get()
    if uname:
        dt = db.user.find_one({'_id': uname})
        if(dt):
            alreadyexists.grid()
        else:
            db.user.insert_one({'_id':uname, 'password':pd})
            registeredyay.grid()
    else:
        cannotbeempty.grid()
Label(ff, text="Login/Register", bg="gray", width="30", height="2", font=("Calibri", 14)).grid()
Label(ff, text="Username", font=("Calibri", 12)).grid(pady=10)
Entry(ff, textvariable=user).grid(pady=2) #username
Label(ff, text="Password", font=("Calibri", 12)).grid(pady=5)
Entry(ff, textvariable=pwd).grid(pady=2) #password
Button(ff, text="Login", height="2", width="10", command=login).grid(pady=10)
Button(ff, text="Register", height="2", width="10", command=register).grid(pady=10)
ff.grid()
