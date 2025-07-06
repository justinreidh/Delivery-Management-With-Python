import csv
from datetime import timedelta

import package
from hashTable import ChainingHashTable
from package import Package
from truck import Truck

#function to load in the data from packageData.csv
def loadPackageData(filename):
    with open(filename) as packageFile:
        packageData = csv.reader(packageFile, delimiter=',')
        for row in packageData:
            packageID = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipCode = row[4]
            deadline = row[5]
            weight = row[6]
            note = row[7]


            newPackage = Package(packageID, address, deadline, city, zipCode, weight, note)
            myHash.insert(packageID, newPackage)

myHash = ChainingHashTable()

loadPackageData('packageData.csv')

#load the distance data
distanceData = []
def loadDistanceData(filename):
    with open(filename) as distanceFile:
        reader = csv.reader(distanceFile, delimiter=',')
        for row in reader:
            distanceData.append(row)

loadDistanceData('distanceData.csv')

#load the address data
addressData = []
def loadAddressData(filename):
    with open(filename) as addressFile:
        reader = csv.reader(addressFile, delimiter=',')
        for row in reader:
            addressData.append(row[0].strip())

loadAddressData('addressData.csv')

#return the distance between two addresses:
def distanceBetween(address1, address2):
    addressIndex1 = addressData.index(address1)
    addressIndex2 = addressData.index(address2)
    if addressIndex1 < addressIndex2:
        return distanceData[addressIndex2][addressIndex1]
    return distanceData[addressIndex1][addressIndex2]

#nearest neighbor algorithm to find minimum distance and address:
def minDistanceFrom(fromAddress, truckPackages):
    i = 0
    minDistance = float('inf')
    minDistancePackage = ''
    while i < len(truckPackages):
        currDistance = distanceBetween(fromAddress, truckPackages[i].address)
        currDistance = float(currDistance)
        if currDistance < minDistance:
            minDistance = currDistance
            minDistancePackage = truckPackages[i]

        i += 1
    return minDistance, minDistancePackage

#set global variables to use in the delivery functions
truck1 = Truck("Truck 1")
truck2 = Truck("Truck 2")
loadNext = True
totalDistance = 0
truck1Time = timedelta(hours=8)
truck2Time = timedelta(hours=8)

#logic for loading packages and updating status
def assignPackages(packages, truck):
    if not loadNext:
        return
    for id in packages:
        newPackage = myHash.search(id)
        truck.addPackage(newPackage)
        newPackage.status = "en Route"

#manually load the packages for the trucks for each load:
def loadFirstPackages():
    firstPackagesID = [1, 4, 7, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 39, 40]
    assignPackages(firstPackagesID, truck1)

def loadSecondPackages():
    secondPackagesTrip1 = [11, 12, 18, 23]
    assignPackages(secondPackagesTrip1, truck2)

def loadThirdPackages():
    secondPackagesTrip2 = [2, 3, 5, 6, 10, 24, 25, 26, 28, 31, 32, 33, 36, 37, 38]
    assignPackages(secondPackagesTrip2, truck2)

def loadFourthPackages():
    secondPackagesTrip3 = [9, 17, 22, 27, 35]
    assignPackages(secondPackagesTrip3, truck2)

#calculate time to complete a delivery
def deliveryTime(distance):
    travelSeconds = (distance/18) * 3600
    travelTime = timedelta(seconds=travelSeconds)
    return travelTime

#deliver packages
def deliverPackages(truck, totalDistance, truckTime, loadNext, inputTime = timedelta(hours=18)):
    #loop through each package, find the nearest address, and update the time and distance
    while truck.packages and inputTime > truckTime:
        newDistance, newPackage = minDistanceFrom(truck.currentAddress, truck.packages)
        travelTime = deliveryTime(newDistance)
        if truckTime + travelTime > inputTime:
            loadNext = False
            return  totalDistance, truckTime, loadNext
        truckTime = truckTime + travelTime
        totalDistance += newDistance
        truck.setAddress(newPackage.address)
        newPackage.status = "Delivered at: " + str(truckTime)
        truck.removePackage(newPackage)
    if truckTime > inputTime:
        loadNext = False
        return totalDistance, truckTime, loadNext
    #calculate the time and distance it takes to return to the hub
    distanceToStation = distanceBetween(truck.currentAddress, "HUB")
    distanceToStation = float(distanceToStation)
    travelTime = deliveryTime(distanceToStation)
    truckTime = truckTime + travelTime
    totalDistance += distanceToStation
    return totalDistance, truckTime, loadNext

#printing function for the user interface
def printAll(packageID):
    if packageID != 100:
        newPackage = myHash.search(packageID)
        print(newPackage)
        print("Total distance: " + str(totalDistance))
        return
    for bucket in myHash.table:
        for key, item in bucket:
            print(item)
    print("Total distance: " + str(totalDistance))
    print("Total time: " + str(truck2Time))
    print("Packages in truck 1: ")
    if not truck1.packages:
        print("No packages left in truck 1")
    else:
        for package in truck1.packages:
            print(package)
    print("Packages in truck 2: ")
    if not truck2.packages:
        print("No packages left in truck 2")
    else:
        for package in truck2.packages:
            print(package)

#Sequentially load the vans and then complete the deliveries, updating the global variables each time
def runAllDeliveries(inputTime, packageID = 100):
    global truck1, truck2, loadNext, totalDistance, truck1Time, truck2Time

    truck1 = Truck("Truck 1")
    truck2 = Truck("Truck 2")
    loadPackageData("packageData.csv")
    loadNext = True
    totalDistance = 0
    truck1Time = timedelta(hours=8)
    truck2Time = timedelta(hours=8)

    loadFirstPackages()
    loadSecondPackages()
    totalDistance, truck1Time, loadNext = deliverPackages(truck1, totalDistance, truck1Time, loadNext, inputTime)
    totalDistance, truck2Time, loadNext = deliverPackages(truck2, totalDistance, truck2Time, loadNext, inputTime)
    loadThirdPackages()
    totalDistance, truck2Time, loadNext = deliverPackages(truck2, totalDistance, truck2Time, loadNext, inputTime)
    if inputTime > timedelta(hours=10, minutes=20):
        package9 = myHash.search(9)
        package9.address = "410 S State St"
    loadFourthPackages()
    totalDistance, truck2Time, loadNext = deliverPackages(truck2, totalDistance, truck2Time, loadNext, inputTime)
    printAll(packageID)

def menu():
    while True:
        print("--------------------------------")
        print("Delivery Simulation")
        print("Menu:")
        print("1. View Total Mileage and all Package Status")
        print("2. View all package status with a time")
        print("3. Look up a single package with a time")
        print("4. Exit")
        selection = input("Select an option: ")

        if selection == "1":
            runAllDeliveries(timedelta(hours=18))
        elif selection == "2":
            hour = int(input("Enter hour (military time): "))
            minute = int(input("Enter minute: "))
            inputTime = timedelta(hours=hour, minutes=minute)
            runAllDeliveries(inputTime)
        elif selection == "3":
            packageID = int(input("Enter package ID: "))
            hour = int(input("Enter hour (military time): "))
            minute = int(input("Enter minute: "))
            inputTime = timedelta(hours=hour, minutes=minute)
            runAllDeliveries(inputTime, packageID)
        elif selection == "4":
            print("Exiting")
            break
        else:
            print("Invalid input")

menu()

















