from tkinter import *
from pymongo import MongoClient
from random import randint

constring='mongodb+srv://disc0nnctd:dc123@dbmspl-e3fyk.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(constring)
db=client.users
#db.user.create_index('phone')

res="450x600"
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
    #--------------------
    def __init__(self):
        self.user=StringVar()
        self.pwd=StringVar()
        self.authsuccess=False
        self.phone=None
        self.userEntry=Entry(ff, textvariable=self.user, width=30)
        self.passEntry=Entry(ff, textvariable=self.pwd, width=30)
    def maketitle(self, text):
        self.title=Label(window, text=text, bg="gray", width="38", height="2", font=("Calibri", 17))
    def forgetmessages():
        UserLogin.cannotbeempty.grid_forget()
        UserLogin.authenticatedstring.grid_forget()
        UserLogin.invaliduserpass.grid_forget()
        UserLogin.pleaseregister.grid_forget()
        UserLogin.alreadyexists.grid_forget()
        UserLogin.registeredyay.grid_forget()
    
    def widgetsAction(self, action):
        widgetVars=['regbutton','loginbutton','userEntry','passEntry']
        for i in widgetVars:
            exec("self.%s.configure(state='%s')"%(i, action))
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
                    self.page1()
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
        def otp():
            self.widgetsAction('disabled')
            self.tempwin=Frame(window)
            tempwin=self.tempwin
            phonealready=Label(tempwin, text="Phone already exists!")
            invalidN=Label(tempwin, text="Invalid Number!")
            invalidOTP=Label(tempwin, text="Invalid OTP!")
            otp=StringVar()
            phn=StringVar()
            self.totp=0
            tempframe=Frame(tempwin)
            tempwin.grid()
            def getotp():
                phonealready.grid_forget()
                invalidOTP.grid_forget()
                invalidN.grid_forget()
                self.totp=randint(1000, 9999)####
                if len(phn.get())==10 and phn.get().isdigit():
                    dt = db.user.find_one({'phone': int(phn.get())})
                    if not dt:
                        print(self.totp)
                        tempframe.grid(padx=5, columnspan=3)
                    else:
                        tempframe.grid_forget()
                        phonealready.grid()
                else:
                    tempframe.grid_forget()
                    invalidN.grid()

            def checkotp():
                phonealready.grid_forget()
                invalidN.grid_forget()
                invalidOTP.grid_forget()
                if str(self.totp)==otp.get():
                    self.phone=phn.get()
                    db.user.insert_one({'_id':uname, 'password':pd, 'phone':int(self.phone)})
                    UserLogin.registeredyay.grid()
                    self.widgetsAction('normal')
                    tempwin.destroy()
                else:
                    invalidOTP.grid()
            Label(tempframe, text="OTP", font=("Calibri")).grid(row=0, column=0)
            Entry(tempframe, textvariable=otp).grid(row=0, column=1)
            Button(tempframe, text="Submit", command=checkotp).grid(row=0, column=2)
            Label(tempwin, text="Phone Number", font=("Calibri")).grid(row=0, column=0, padx=5)
            Entry(tempwin, textvariable=phn).grid(row=0, column=1)
            Button(tempwin, text="Get OTP", command=getotp).grid(row=0, column=2)

        
        if uname:
            dt = db.user.find_one({'_id': uname})
            if(dt):
                UserLogin.alreadyexists.grid()
            else:
                otp()
        else:
            UserLogin.cannotbeempty.grid()
    def generate1(self):
        self.maketitle("Login/Register")
        self.title.grid()
        Label(ff, text="Username", font=("Calibri", 15)).grid(pady=5)
        self.userEntry.grid(pady=2)
        Label(ff, text="Password", font=("Calibri", 15)).grid(pady=5)
        self.passEntry.grid(pady=2)
        self.loginbutton=Button(ff, text="Login", height="2", width="15", command=self.login)
        self.loginbutton.grid(pady=10)
        self.regbutton=Button(ff, text="Register", height="2", width="15", command=self.register)
        self.regbutton.grid(pady=10)
        ff.grid(pady=80)
    def suicide(self):
        ff.destroy()
        self.title.grid_forget()

    def userdriverotp(self):
        pass
        #display otp to user
        #save otp to driver db
        #take otp from driver
        #delete otp if match
        #return true if match
    def page1(self):
        global ff
        ff=Frame(window)
        self.maketitle("Welcome %s"%self.user.get())
        self.title.grid()

        locations=[]
        #where from (dropdown)
        #where to (dropdown)
        
        #class (dropdown)
        #calculatedistance(label)
        #price
        #store time
        #next page
        

        ff.grid()
    def page2(self):
        pass
        #looking for ride
        #ride found

        #fetch driver details

        #get otp
        #wait for driver to enter otp to start ride
        #next page
    def page3(self):
        pass
        #ride active
        #reached location
        #get otp
        #driver enter otp
        #rate the driver (radio button)
    
a=UserLogin()
a.generate1()
