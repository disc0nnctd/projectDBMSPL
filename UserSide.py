from tkinter import *
from pymongo import MongoClient
from random import randint
from datetime import datetime
from geopy.distance import great_circle
#great_circle(loc1, loc2).km distance

constring='mongodb+srv://disc0nnctd:dc123@dbmspl-e3fyk.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(constring)
db=client.users

loc=client.locations.location

#db.user.create_index('phone')

res="450x600"
window=Tk()
window.geometry(res)
window.resizable(width=False, height=False)
window.title("notUber")
ff=Frame(window)

class UserLogin:
    def maketitle(self, text):
        self.title=Label(window, text=text, bg="gray", width="38", height="2", font=("Calibri", 17))
    def suicide(self):
        ff.destroy()
        self.title.grid_forget()
    def __init__(self):
            self.user=StringVar()
            self.pwd=StringVar()
            self.authsuccess=False
            self.phone=None
            userEntry=Entry(ff, textvariable=self.user, width=30)
            passEntry=Entry(ff, textvariable=self.pwd, width=30)
            loginbutton=Button(ff, text="Login", height="2", width="15")
            regbutton=Button(ff, text="Register", height="2", width="15")
            
            #---MessageLabels----
            cannotbeempty=Label(ff, text="Fields cannot be empty!", fg="red")
            authenticatedstring=Label(ff, text="Authenticated!")
            invaliduserpass=Label(ff, text="Invalid Username/Password pair. Try again.", fg="red")
            pleaseregister=Label(ff, text="Please register.", fg="red")
            alreadyexists=Label(ff, text="User already exists!", fg="red")
            registeredyay=Label(ff, text="Registered! Try logging in!")
            #---MessageLabels----
            
            def forgetmessages():
                cannotbeempty.grid_forget()
                authenticatedstring.grid_forget()
                invaliduserpass.grid_forget()
                pleaseregister.grid_forget()
                alreadyexists.grid_forget()
                registeredyay.grid_forget()
            def widgetsAction(action):
                regbutton.configure(state=action)
                loginbutton.configure(state=action)
                userEntry.configure(state=action)
                passEntry.configure(state=action)
                
                
            def login():
                forgetmessages()
                uname=self.user.get()
                pd=self.pwd.get()
                if(uname and pd):
                    dt = db.user.find_one({'_id': uname})
                    if(dt):
                        if dt['password']==pd:
                            authenticatedstring.grid()
                            #next window
                            self.authsuccess=True
                            self.suicide()
                            self.page1()
                        else:
                            invaliduserpass.grid()
                    else:
                        pleaseregister.grid()
                else:
                    cannotbeempty.grid()
            def register():
                forgetmessages()
                uname=self.user.get()
                pd=self.pwd.get()
                def otp():
                    widgetsAction('disabled')
                    self.tempwin=Frame(window)
                    tempwin=self.tempwin
                    #---MessageLabels----
                    phonealready=Label(tempwin, text="Phone already exists!", fg="red")
                    invalidN=Label(tempwin, text="Invalid Number!", fg="red")
                    invalidOTP=Label(tempwin, text="Invalid OTP!", fg="red")
                    #---MessageLabels----
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
                            registeredyay.grid()
                            widgetsAction('normal')
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
                        alreadyexists.grid()
                    else:
                        otp()
                else:
                    cannotbeempty.grid()
            def generate():
                self.maketitle("Login/Register")
                self.title.grid()
                Label(ff, text="Username", font=("Calibri", 15)).grid(pady=5)
                userEntry.grid(pady=2)
                Label(ff, text="Password", font=("Calibri", 15)).grid(pady=5)
                passEntry.grid(pady=2)
                loginbutton.configure(command=login)
                loginbutton.grid(pady=10)
                regbutton.configure(command=register)
                regbutton.grid(pady=10)
                ff.grid(pady=80)
            generate()

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
        self.maketitle("Welcome %s!"%self.user.get())
        self.title.grid()
        
        #-------MessageLabels--------
        pleaseselectsrcdest= Label(ff, text="Please select a source and adestionation!", fg='red')
        locationscantbesame= Label(ff, text="Source and Destination cannot be same!", fg='red')
        lookingforaride=Label(ff, text="Looking for a ride....")
        #somelabel= Label(ff, text="somemessage", fg='red')
        
        
        #-------MessageLabels--------

        def delmessagelabels():
            pleaseselectsrcdest.grid_forget()
            locationscantbesame.grid_forget()
            lookingforaride.grid_forget()

        def disableoptions():
            srcmenu.configure(state="disabled")
            destmenu.configure(state="disabled")
        def getDistance(a,b):
            la = readFromDB(a)
            lb = readFromDB(b)
            print("distance is %.01f km"%great_circle(la, lb).km)
        
        def readLocFromDB(name):
            x=loc.find_one({"name":name})
            print(x)
            lat=x['lat']
            lng=x['lng']
            return (lat, lng)
        
        def loadLocsFromDB():
            y=loc.find({}, {"name":1, "_id":0}) #get all "name" from collection, exclude "_id"
            locations=[j['name'] for j in y]
            return locations
        
        def submitButton():
            delmessagelabels()
            s=self.src.get()
            d=self.dest.get()
            if(s and d):
                if(s!=d):
                    disableoptions()
                    lookingforaride.grid()
                else:
                    locationscantbesame.grid()
            else:
                pleaseselectsrcdest.grid()
                
                
        
        timenow=datetime.now()
        self.date=str(timenow.date())
        self.time=timenow.time().strftime("%H:%M:%S")
        locsavl=loadLocsFromDB()

        self.wherefrom=StringVar()
        
        self.src=StringVar()
        self.dest=StringVar()
        self.dist=0.0
        self.type=StringVar()


        Label(ff, text="Source", font=("Calibri", 13)).grid(pady=5)
        srcmenu = OptionMenu(ff, self.src, *locsavl)
        srcmenu.grid() #unpacks locations list
        
        Label(ff, text="Destination", font=("Calibri", 13)).grid(pady=5)
        destmenu=OptionMenu(ff, self.dest, *locsavl)
        destmenu.grid() #unpacks locations list

        Button(ff, text="Submit", command=submitButton).grid(pady=5)
        
        
        
        #where from (dropdown)
        #self.frommenu=
        #where to (dropdown)
        
        #class (dropdown)
        #calculatedistance(label)
        #price
        #store time
        #suicide()
        #next page
        

        ff.grid()
    def page2(self):
        pass
        #looking for ride
        #ride found

        #fetch driver details
        
        #get otp
        #wait for driver to enter otp to start ride
        #suicide()
        #next page
    def page3(self):
        pass
        #ride active
        #reached location
        #get otp
        #driver enter otp
        #suicide()
        #rate the driver (radio button)
    
a=UserLogin()
