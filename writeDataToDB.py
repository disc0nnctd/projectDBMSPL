from pymongo import MongoClient
import csv
from geopy.distance import great_circle
#great_circle(loc1, loc2).km distance


constring='' #mongodb connection string
client=MongoClient(constring)
loc=client.data.location
vehicl=client.data.vehicle
driver=client.data.driver

def writeToDB(id, name, lat, lng):
##    with open('coords.csv') as csv_file:
##        csv_reader = csv.reader(csv_file, delimiter=';')
##        id=101
##        for row in csv_reader:
##            name=row[0]
##            lat=float(row[1])
##            lng=float(row[2])
    loc.insert_one({"_id":id, "name":name, "lat":lat, "lng":lng})
#          id+=1
def readFromDB(name):
    x=loc.find_one({"name":name})
    print(x)
    lat=x['lat']
    lng=x['lng']
    return (lat, lng)

def getDistance(a,b):
    la = readFromDB(a)
    lb = readFromDB(b)
    print("distance is %.01f km"%great_circle(la, lb).km)
def loadLocsFromDB():
    y=loc.find({}, {"name":1, "_id":0})
    locations=[j['name'] for j in y]
    return locations

#   vehicl.create_index('name')
def writeType(name, seats, price=10):
    vehicl.insert_one({"_id":name, "seats":seats, "price":price})

def loadTypesFromDB():
    y=vehicl.find({}, {"name":1,"seats":1, "_id":0}) #get all "name", "seats" from collection, exclude "_id"
    typs={j['name']:j['seats'] for j in y}
    return typs

def addDriver(name, password, vehicle, phone):
    driver.insert_one({"_id":name,"password":password,"type":vehicle,"phone":phone, "rating":0, "rides":0})

