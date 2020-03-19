from tkinter import *
from tkinter import ttk
from pymongo import MongoClient

constring='mongodb+srv://disc0nnctd:dc123@dbmspl-e3fyk.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(constring)
db=client.data

#db=client.testing
loc=db.location
vehicles=db.vehicle
#db.user.create_index('phone')

res="450x600"
window=Tk()
window.geometry(res)
window.resizable(width=False, height=False)
window.title("notUberDriver")
ff=Frame(window)

def nothing():
    pass

class DriverLogin:
    def maketitle(self, text):
        self.title=Label(window, text=text, bg="black", width="38", height="2", fg="white", font=("Calibri", 17))
    def makeff(self, title):
        global ff
        ff=Frame(window)
        self.maketitle(title)
        self.title.grid()
    def suicide(self):
        ff.destroy()
        self.title.grid_forget()
    
    def __init__(self):
            self.user=StringVar()
            self.pwd=StringVar()
            self.username=''
            self.type=None
            self.authsuccess=False
            self.phone=None

            userEntry=ttk.Entry(ff, textvariable=self.user, width=30)
            passEntry=ttk.Entry(ff, textvariable=self.pwd, width=30, show="*")
            loginbutton=Button(ff, text="Login", height="2", width="15")
            #---MessageLabels----
            cannotbeempty=Label(ff, text="Fields cannot be empty!", fg="red")
            authenticatedstring=Label(ff, text="Authenticated!")
            invaliduserpass=Label(ff, text="Invalid Username/Password pair. Try again.", fg="red")
            notexist=Label(ff, text="User does not exist!", fg="red")
            alreadyexists=Label(ff, text="User already exists!", fg="red")
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
                            #next window
                            self.page1()
                        else:
                            invaliduserpass.grid()
                    else:
                        notexist.grid()
                else:
                    cannotbeempty.grid()
            def generate():
                self.maketitle("Login")
                self.title.grid()
                Label(ff, text="Username", font=("Calibri", 15)).grid(pady=5)
                userEntry.grid(pady=2)
                Label(ff, text="Password", font=("Calibri", 15)).grid(pady=5)
                passEntry.grid(pady=2)
                loginbutton.configure(command=login)
                loginbutton.grid(pady=10)
                ff.grid(pady=80)
            generate()
    def page1(self):
        self.suicide()
        self.makeff("Welcome %s!"%self.user.get())
        Label(ff, text="Select a ride:", font=("Calibri", 15)).grid(pady=5)
        #--------MessageLabels--------------
        noridesfound=Label(ff, text="No rides found!")
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
        
        avlrides=ttk.Treeview(ff, columns=(details), show="headings", height=5)
        for i in range(len(details)):
            exec("avlrides.heading('#%s', text='%s')"%(i+1, details[i]))
            exec("avlrides.column('#%s', width=70)"%(i+1))
        avlrides.column('#1', width=30)
        avlrides.column('#2', width=100)
        avlrides.column('#3', width=100)
        
        enableTree()
        avlrides.grid(pady=5)
        refreshbutton=Button(ff, text="Refresh", height="2", width="15", command=fetchrides)
        refreshbutton.grid(pady=5)

        submitbutton=Button(ff, text="Submit", height="2", width="15", command=getride)
        submitbutton.grid(pady=5)
        
        fetchrides()
        ff.grid(pady=50)
    def page2(self):
        self.suicide()
        self.makeff("Activate Ride")

        #-------MessageLabels------
        otpwrong=Label(ff, text="OTP incorrect!", font=("Calibri", 13), fg='red')
        #-------------------------
        def checkOTP():
            if(enteredotp.get()==otp):
                db.otps.update_one({'_id':self.rideid}, {'$set':{'status':'active'}})
                self.page3()
            else:
                otpwrong.grid()
        
        ride=None
        otp=None

        while not ride:
            try:
                ride=db.activerides.find_one({'_id':self.rideid})
            except:
                continue
        while not otp:
            try:
                otp= db.otps.find_one({'_id':self.rideid})['sotp']
            except:
                continue
        enteredotp=IntVar()
        
        Label(ff, text="User: %s"%ride['user'], font=("Calibri", 13)).grid(pady=5)
        Label(ff, text="OTP:", font=("Calibri", 13)).grid(pady=5)
        ttk.Entry(ff, textvariable=enteredotp, width=10).grid(pady=5)
        
        Button(ff, text="Submit", height="2", width="15", command=checkOTP).grid()
        ff.grid(pady=100)
    
    def page3(self):
        self.suicide()
        self.makeff("Ride Active")
        def setEnd():
            db.otps.update_one({'_id':self.rideid}, {'$set':{'status':'end'}})
            self.page4()
        Button(ff, text="End Ride", height="2", width="15", command=setEnd).grid()
        ff.grid(pady=100)
    def page4(self):
        self.suicide()
        self.makeff("Ride End OTP")
        
        #-------MessageLabels------
        otpwrong=Label(ff, text="OTP incorrect!", font=("Calibri", 13), fg='red')
        #-------------------------
        def checkOTP():
            if(enteredotp.get()==otp):
                db.otps.update_one({'_id':self.rideid}, {'$set':{'status':'done'}})
                self.suicide()
                self.makeff("Ride Complete!")
            else:
                otpwrong.grid()
    
        otp=None
        while not otp:
            try:
                otp= db.otps.find_one({'_id':self.rideid})['rotp']
            except:
                continue
        enteredotp=IntVar()
        Label(ff, text="OTP:", font=("Calibri", 13)).grid(pady=5)
        ttk.Entry(ff, textvariable=enteredotp, width=30).grid(pady=5)
        Button(ff, text="Submit", height="2", width="15", command=checkOTP).grid()
        ff.grid(pady=100)
a=DriverLogin()
window.mainloop()
