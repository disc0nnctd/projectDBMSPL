from pymongo import MongoClient
import csv
from geopy.distance import great_circle
#great_circle(loc1, loc2).km distance


constring='mongodb+srv://disc0nnctd:dc123@dbmspl-e3fyk.mongodb.net/test?retryWrites=true&w=majority'
client=MongoClient(constring)
loc=client.data.location
vehicl=client.data.vehicle

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
    global y
    y=loc.find({}, {"name":1, "_id":0})

#   vehicl.create_index('name')
def writeClass(name, seats, price):
    vehicl.insert_one({"name":name, "seats":seats, "price":price})
    
    
