"""https://github.com/disc0nnctd/projectDBMSPL.git"""

from tkinter import *
from tkinter import ttk
from pymongo import MongoClient

constring='mongodb+srv://disc0nnctd:dc123@dbmspl-e3fyk.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(constring)
db=client.data

res="450x600"
window2=Tk()
window2.geometry(res)
window2.resizable(width=False, height=False)
window2.title("notUberDriver")
ff2=Frame(window2)

def nothing():
    pass

class DriverLogin:
    def maketitle(self, text):
        self.title=Label(window2, text=text, bg="black", width="38", height="2", fg="white", font=("Calibri", 17))
    def makeff2(self, title):
        global ff2
        ff2=Frame(window2)
        self.maketitle(title)
        self.title.grid()
    def suicide(self):
        ff2.destroy()
        self.title.grid_forget()
    
    def __init__(self):
            self.user=StringVar()
            self.pwd=StringVar()
            self.username=''
            self.type=None
            self.authsuccess=False
            self.phone=None

            userEntry=ttk.Entry(ff2, textvariable=self.user, width=30)
            passEntry=ttk.Entry(ff2, textvariable=self.pwd, width=30, show="*")
            loginbutton=Button(ff2, text="Login", height="2", width="15")
            #---MessageLabels----
            cannotbeempty=Label(ff2, text="Fields cannot be empty!", fg="red")
            authenticatedstring=Label(ff2, text="Authenticated!")
            invaliduserpass=Label(ff2, text="Invalid Username/Password pair. Try again.", fg="red")
            notexist=Label(ff2, text="User does not exist!", fg="red")
            alreadyexists=Label(ff2, text="User already exists!", fg="red")
            #---MessageLabels----

            def forgetmessages():
                cannotbeempty.grid_forget()
                authenticatedstring.grid_forget()
                invaliduserpass.grid_forget()
                notexist.grid_forget()
                alreadyexists.grid_forget()
            def widgetsAction(action):
                loginbutton.configure(state=action)
                userEntry.configure(state=action)
                passEntry.configure(state=action)
            
            def login():
                forgetmessages()
                uname=self.user.get()
                pd=self.pwd.get()
                if(uname and pd):
                    dt = db.driver.find_one({'_id': uname})
                    if(dt):
                        if dt['password']==pd:
                            authenticatedstring.grid()
                            self.username=uname
                            self.type=dt['type']
                            self.authsuccess=True
                            #next window2
                            self.page1()
                        else:
                            invaliduserpass.grid()
                    else:
                        notexist.grid()
                else:
                    cannotbeempty.grid()
            def generate():
                self.maketitle("Driver Login")
                self.title.grid()
                Label(ff2, text="Username", font=("Calibri", 15)).grid(pady=5)
                userEntry.grid(pady=2)
                Label(ff2, text="Password", font=("Calibri", 15)).grid(pady=5)
                passEntry.grid(pady=2)
                loginbutton.configure(command=login)
                loginbutton.grid(pady=10)
                ff2.grid(pady=80)
            generate()
    def page1(self):
        self.suicide()
        self.makeff2("Welcome %s!"%self.user.get())
        Label(ff2, text="Select a ride:", font=("Calibri", 15)).grid(pady=5)
        #--------MessageLabels--------------
        noridesfound=Label(ff2, text="No rides found!")
        #----------------------------

        def forgetmessages():
            noridesfound.grid_forget()
            
       
            
        def handle_click(event):                                             
            if avlrides.identify_region(event.x, event.y) == "separator": #used to prevent resizing of Treeview columns
                return "break"
        def enableTree():
            avlrides.bind("<Button-1>", handle_click) #used to prevent resizing of Treeview columns
        def disableTree():
            avlrides.bind("<<TreeviewSelect>>", lambda _: nothing())  #makes it stop working after submission 

        def fetchrides():
            avlrides.delete(*avlrides.get_children())
            noridesfound.grid_forget()
            try:
                fetchedrides=[i for i in db.avlrides.find({'type':self.type, 'driver':''})] #{'type':self.type}
                for j in fetchedrides:
                    avlrides.insert("", 'end', values=(j['_id'], j['from'], j['to'], j['time'], j['user']))
            except:
                noridesfound.grid()

        def getride():
            disableTree()
            self.rideid=avlrides.item(avlrides.focus())['values'][0]
            db.avlrides.update_one({'_id': self.rideid}, {"$set":{'driver':self.username}})

            self.page2()           



        details=["ID", "From", "To", "Time", "Username"]
        
        avlrides=ttk.Treeview(ff2, columns=(details), show="headings", height=5)
        for i in range(len(details)):
            exec("avlrides.heading('#%s', text='%s')"%(i+1, details[i]))
            exec("avlrides.column('#%s', width=70)"%(i+1))
        avlrides.column('#1', width=30)
        avlrides.column('#2', width=100)
        avlrides.column('#3', width=100)
        
        enableTree()
        avlrides.grid(pady=5)
        refreshbutton=Button(ff2, text="Refresh", height="2", width="15", command=fetchrides)
        refreshbutton.grid(pady=5)

        submitbutton=Button(ff2, text="Submit", height="2", width="15", command=getride)
        submitbutton.grid(pady=5)
        
        fetchrides()
        ff2.grid(pady=50)
    def page2(self):
        self.suicide()
        self.makeff2("Activate Ride")

        #-------MessageLabels------
        otpwrong=Label(ff2, text="OTP incorrect!", font=("Calibri", 13), fg='red')
        #-------------------------
        enteredotp=IntVar()

        self.otp=None
        self.ride=None

        def OTPsize(*args): #keeps size limit of OTP entry
            value = enteredotp.get()
            if len(value) > 4: enteredotp.set(value[:4])
        enteredotp.trace('w', OTPsize)
        
        def checkOTP():
            if(enteredotp.get()==str(self.otp)):
                db.otps.update_one({'_id':self.rideid}, {'$set':{'status':'active'}})
                self.page3()
            else:
                print(type(enteredotp.get()))
                print(enteredotp.get())
                otpwrong.grid()
        
        def rideExist():
            try:
                ride=db.activerides.find_one({'_id':self.rideid})
                Label(ff2, text="User: %s"%ride['user'], font=("Calibri", 13)).grid(pady=5)
            except:
                window2.after(1000, rideExist)
        
        def otpExist():
            try:
                self.otp= db.otps.find_one({'_id':self.rideid})['sotp']
                Label(ff2, text="OTP:", font=("Calibri", 13)).grid(pady=5)
                ttk.Entry(ff2, textvariable=enteredotp, width=5).grid(pady=5)
                Button(ff2, text="Submit", height="2", width="15", command=checkOTP).grid()
            except:
                window2.after(1000, otpExist)

        rideExist()
        otpExist()
        
        ff2.grid(pady=100)
    
    def page3(self):
        self.suicide()
        self.makeff2("Ride Active")
        def setEnd():
            db.otps.update_one({'_id':self.rideid}, {'$set':{'status':'end'}})
            self.page4()
        Button(ff2, text="End Ride", height="2", width="15", command=setEnd).grid()
        ff2.grid(pady=100)
    def page4(self):
        self.suicide()
        self.makeff2("Ride End OTP")
        
        #-------MessageLabels------
        otpwrong=Label(ff2, text="OTP incorrect!", font=("Calibri", 13), fg='red')
        #-------------------------
        enteredotp=StringVar()
        self.otp=None
        
        def OTPsize(*args): #keeps size limit of OTP entry
            value = enteredotp.get()
            if len(value) > 4: enteredotp.set(value[:4])
        enteredotp.trace('w', OTPsize)
        
        def checkOTP():
            if(enteredotp.get()==str(self.otp)):
                db.otps.update_one({'_id':self.rideid}, {'$set':{'status':'done'}})
                self.suicide()
                self.makeff2("Ride Complete!")
            else:
                otpwrong.grid()
    
        def otpExist():
            try:
                self.otp= db.otps.find_one({'_id':self.rideid})['rotp']
                Label(ff2, text="OTP:", font=("Calibri", 13)).grid(pady=5)
                ttk.Entry(ff2, textvariable=enteredotp, width=5).grid(pady=5)
                Button(ff2, text="Submit", height="2", width="15", command=checkOTP).grid()
            except:
                window2.after(1000, otpExist)
        otpExist()
        
        ff2.grid(pady=100)
b=DriverLogin()
window2.mainloop()
