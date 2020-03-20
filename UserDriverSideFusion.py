"""https://github.com/disc0nnctd/projectDBMSPL.git"""

"""
Since each driver has a specific type of vehicle,
the rides available only for him will be loaded.
for eg.
admin(password: notadming) requests Sedan
driver1(password: 1234) drives Sedan

so only Sedan rides will be loaded for the driver, ie. admin
"""


from tkinter import *
from tkinter import ttk
from pymongo import MongoClient
from random import randint
from datetime import datetime
from geopy.distance import great_circle

#great_circle(loc1, loc2).km distance

now=datetime.now()

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
window.title("notUber")
ff=Frame(window)

def nothing():
    pass

class UserLogin:
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
            self.authsuccess=False
            self.phone=None

            userEntry=ttk.Entry(ff, textvariable=self.user, width=30)
            passEntry=ttk.Entry(ff, textvariable=self.pwd, width=30, show="*")
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
                            self.username=uname
                            self.authsuccess=True
                            #next window
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
                    def OTPsize(*args): #keeps size limit of OTP entry
                        value = otp.get()
                        if len(value) > 4: otp.set(value[:4])
                    otp.trace('w', OTPsize)
                    
                    phn=StringVar()
                    self.totp=0
                    tempframe=Frame(tempwin)
                    tempwin.grid()
                    def getotp():
                        phonealready.grid_forget()
                        invalidOTP.grid_forget()
                        invalidN.grid_forget()
                        self.totp=randint(1000, 9999)####
                        ph=phn.get()
                        if len(ph)==10 and ph.isdigit() and not ph.startswith('0'):
                            dt = db.user.find_one({'phone': int(ph)})
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
                    ttk.Entry(tempframe, textvariable=otp, width=5).grid(row=0, column=1)
                    Button(tempframe, text="Submit", command=checkotp).grid(row=0, column=2)
                    Label(tempwin, text="Phone Number", font=("Calibri")).grid(row=0, column=0, padx=5)
                    ttk.Entry(tempwin, textvariable=phn).grid(row=0, column=1)
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
                self.maketitle("User Login/Register")
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

    def page1(self):
        self.suicide()
        self.makeff("Welcome %s!"%self.user.get())
        timenow=datetime.now()
        self.date=str(timenow.date())
        self.time=timenow.time().strftime("%H:%M:%S")
        self.wherefrom=StringVar()
        self.src=StringVar()
        self.dest=StringVar()

        self.type=StringVar()
        
        self.dist=DoubleVar()
        self.price=DoubleVar()
        baseprice=40        
        
        #-------MessageLabels--------
        pleaseselectsrcdest= Label(ff, text="Please select a source and a destionation!", fg='red')
        locationscantbesame= Label(ff, text="Source and Destination cannot be same!", fg='red')
        selecttype=Label(ff, text="Please select a type of vehicle")
        lookingforaride=Label(ff, text="Looking for a ride....")
        ridenotfound= Label(ff, text="Couldn't find you a ride! Try again later!")
        #somelabel= Label(ff, text="somemessage", fg='red')
        #-------MessageLabels--------
                
        def forgetmessagelabels():
            pleaseselectsrcdest.grid_forget()
            locationscantbesame.grid_forget()
            lookingforaride.grid_forget()
            selecttype.grid_forget()
            ridenotfound.grid_forget()

        def disableoptions():
            srcmenu.configure(state="disabled")
            destmenu.configure(state="disabled")
            subbutton.configure(state="disabled")
            disableTree()
            #vehmenu.configure(state="disabled")
        def enableoptions():
            srcmenu.configure(state="normal")
            destmenu.configure(state="normal")
            subbutton.configure(state="normal")
            enableTree()
        def getDistance(a,b):
            la = readLocFromDB(a)
            lb = readLocFromDB(b)
            #print("distance is %.01f km"%great_circle(la, lb).km)
            return great_circle(la, lb).km
            
        def readLocFromDB(name):
            tmp=loc.find_one({"name":name})
            p=tmp['lat']
            q=tmp['lng']
            return (p, q)
        
        def loadLocsFromDB():
            y=loc.find({}, {"name":1, "_id":0}) #get all "name" from collection, exclude "_id"
            locations=[j['name'] for j in y]
            return locations

        def readTypeFromDB(name):
            tmp=vehicles.find_one({"name":name}, {'price':1, "_id":0}) #get "price" count from given name, exclude "_id"
            t=tmp['price']
            return t
        
        def loadTypesFromDB():
            y=vehicles.find({}, {"name":1,"seats":1, "_id":0}) #get all "name", "seats" from collection, exclude "_id"
            typs={j['name']:j['seats'] for j in y}
            return typs

        def handle_click(event):                                             
            if typeoptions.identify_region(event.x, event.y) == "separator": #used to prevent resizing of Treeview columns
                return "break"
        def enableTree():
            typeoptions.bind("<<TreeviewSelect>>", lambda _:settype())  #lambda _ becuase bind puts an argument in command
            typeoptions.bind("<Button-1>", handle_click) #used to prevent resizing of Treeview columns
            
        def disableTree():
            typeoptions.bind("<<TreeviewSelect>>", lambda _: nothing())  #makes it stop working after submission 
            
        def settype():
            getoption=typeoptions.item(typeoptions.focus())['values'][0]
            #print(getoption)
            self.type.set(getoption)
            updateprice()
        
        def updateprice(): 
            forgetmessagelabels()
            a=self.src.get()
            b=self.dest.get()
            if "Select one" not in (a, b):
                if(a==b):
                    locationscantbesame.grid()
                    subbutton.configure(state="disabled")
                    self.dist.set(0)
                    self.price.set(0)
                else:
                    subbutton.configure(state="normal")
                    dista=getDistance(a, b)
                    self.dist.set(round(dista, 2))
                    x=self.type.get()
                    if x:
                        prce=readTypeFromDB(x)
                        self.price.set(round(prce+baseprice+(dista*25), 2))
        def genID():
            p=True
            q=True
            r=True
            while p or q or r:
                genid=randint(100,999)
                p=db.activeride.find_one({'_id':genid})
                q=db.pastrides.find_one({'_id':genid})
                r=db.avl.find_one({'_id':genid})
            return genid
        
        def driverUpdate():
            a=db.avlrides.find_one(self.ridedetails)['driver']
            if a:
                self.udriver=a
                self.page2()
                return
            else:
                if self.timeout>0:
                    self.timeout-=1
                    #print(self.timeout)
                    window.after(1000, driverUpdate)
                else:
                    forgetmessagelabels()
                    db.avlrides.delete_one(self.ridedetails)
                    enableoptions()
                    ridenotfound.grid()
        
        def uploadSearch(s, d, t):
            lookingforaride.grid()
            now=datetime.now()
            date=now.strftime("%Y-%m-%d")
            time=now.strftime("%H:%M:%S")
            foundRide=False
            self.rideid= genID()
            self.ridedetails={'_id':self.rideid, 'from': s, 'to':d, 'time': time, 'date': date, 'type': t, 'user': self.username}
            db.avlrides.insert_one(self.ridedetails)
            db.avlrides.update_one(self.ridedetails, {"$set": {'driver':''}})
            self.udriver=None
            self.timeout=120
            driverUpdate()
            
        def submitButton():
            forgetmessagelabels()
            s=self.src.get()
            d=self.dest.get()
            t=self.type.get()
            if "Select one" not in (s and d):
                if(s!=d):
                    if t:
                        disableoptions()
                        uploadSearch(s, d, t)
                        
                    else:
                        selecttype.grid()
                else: # dont need to put this since the submit button gets disabled when same locations set
                    locationscantbesame.grid()
            else:
                pleaseselectsrcdest.grid()
        
        
        locsavl=loadLocsFromDB() #list of names of locations

        types=loadTypesFromDB() # {name:seats}
                                                
        Label(ff, text="Source", font=("Calibri", 13)).grid(pady=5)
    
        srcmenu = ttk.OptionMenu(ff, self.src, "Select one", *locsavl, command=lambda _:updateprice()) # * unpacks locations list  #lambda _ becuase optionmenu puts an argument in command
        srcmenu.grid()
        
        Label(ff, text="Destination", font=("Calibri", 13)).grid(pady=5)
        destmenu=ttk.OptionMenu(ff, self.dest, "Select one", *locsavl, command=lambda _:updateprice()) #lambda _ becuase optionmenu puts an argument in command
        destmenu.grid()

        Label(ff, text="Vehicle:", font=("Calibri", 13)).grid(pady=5)

        typeoptions=ttk.Treeview(ff, columns=("Type", "Seats"), show="headings", height=5)
        typeoptions.heading('#1', text='Type')
        typeoptions.heading('#2', text='Seats')
        typeoptions.column("#1", width=70)
        typeoptions.column("#2", width=50)
        for i in types:
            typeoptions.insert("", 'end', values=(i, types[i]))
        enableTree()
        typeoptions.grid()


        Label(ff, text="Distance(KM)", font=("Calibri", 13)).grid(pady=5)
        distancebox=Label(ff, textvariable=self.dist, width=6, borderwidth=2, relief="sunken").grid(pady=5)

        Label(ff, text="Price(Rupees)", font=("Calibri", 13)).grid(pady=5)
        pricebox=Label(ff, textvariable=self.price, width=6, borderwidth=2, relief="sunken").grid(pady=5)

        subbutton=Button(ff, text="Submit", command=submitButton)
        
        subbutton.grid(pady=5)
        
        ff.grid()

    def page2(self):
        def activateRide(): #when driver updates status to active
            status=db.otps.find_one({'_id': self.rideid})['status']
            if status == 'active':
                ot.grid_forget()
                activeride.grid()
                checkComplete()
                return
            window.after(1000, activateRide)
        def checkComplete():  #to comfirm if ride is done
            status=db.otps.find_one(self.rideid)['status']
            if status=='end':
                rotp=randint(1000, 9999)
                Label(ff, text="End OTP: %s"%rotp, font=("Calibri", 13)).grid(pady=5)
                db.otps.update_one({'_id':self.rideid}, {"$set":{'rotp':rotp}})
                activeride.grid_forget()
                endRide()
                return
            window.after(1000, checkComplete)
                    
        def endRide():
            status=db.otps.find_one(self.rideid)['status']
            if status=='done':
                self.page3()
                return
            window.after(1000, endRide)
            
        self.suicide()
        #driver is self.udriver
        driver=db.driver.find_one({'_id': self.udriver})
        self.makeff("Ride Details")

        activeride=Label(ff, text="Ride is active.", font=("Calibri", 13), borderwidth=2, relief="sunken", bg="white")
        
        db.avlrides.delete_one(self.ridedetails)
        db.activerides.insert_one(self.ridedetails)
        db.activerides.update_one(self.ridedetails, {"$set": {'driver': self.udriver}})
        
        Label(ff, text="Driver ID: %s"%driver['_id'], font=("Calibri", 13)).grid(pady=100)
        Label(ff, text="Contact: %s"%driver['phone'], font=("Calibri", 13)).grid(pady=5)

        sotp=randint(1000, 9999)
        #db.activerides.update_one(self.ridedetails, {"$set":{'sotp':sotp}})
        
        db.otps.insert_one({'_id':self.rideid, 'sotp':sotp, 'status':'otp'})  #status will be set by driver side, 'done' when driver presses button that the ride is done
        ot=Label(ff, text="Start OTP: %s"%sotp, font=("Calibri", 13))
        ot.grid(pady=5)
        ff.grid()
        activateRide()
        #checkComplete()
        #driver side will delete the ride from active and move it to pastrides
    def page3(self):
        self.suicide()
        self.makeff("Ride Complete")
        pleaseselect=Label(ff, text= "Please select a rating!", font=("Calibri", 13))
        
        def submit():
            rating=rate.get()
            if rating != 0:
                pleaseselect.grid_forget()
                rateride.grid_forget()
                rbns.grid_forget()
                sub.grid_forget()
                Label(ff, text= "Thank you!", font=("Calibri", 13)).grid(pady=200)
                
                driver=db.driver.find_one({'_id': self.udriver})
                rides=driver['rides'] + 1
                newrating= (driver['rating'] + rating)/rides
                db.driver.update_one({'_id':self.udriver}, {'$set':{'rating':newrating, 'rides':rides}})

                db.activerides.delete_one({'_id': self.rideid})

                db.pastrides.insert_one(self.ridedetails)
                db.pastrides.update_one(self.ridedetails, {"$set": {'driver': self.udriver, 'rating': rating}})
            else:
                pleaseselect.grid()
        
        rateride= Label(ff, text= "Rate your ride", font=("Calibri", 13))
        rateride.grid(pady=100)
        rate=IntVar()
        rbns=Frame(ff)
        for i in range(5):
            Radiobutton(rbns, text=i+1, variable=rate, value= i+1, command=pleaseselect.grid_forget).grid(row=0, column=i)
        rbns.grid()
        
        sub= Button(ff, text="Submit", height="2", width="15", command=submit)
        sub.grid()
        ff.grid()        

#----------------------------------------------------Driver Side-----------------------------------------------------

window2=Toplevel()
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
        Label(ff2, text="You drive a %s."%self.type, font=("Calibri", 15)).grid(pady=5)
        Label(ff2, text="Available rides:", font=("Calibri", 15)).grid(pady=5)
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
        enteredotp=StringVar()
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


a=UserLogin()

b=DriverLogin()

window.mainloop()

window2.mainloop()
