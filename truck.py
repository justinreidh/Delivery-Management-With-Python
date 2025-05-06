class Truck:
    def __init__(self, name, capacity=16, currentAddress = "HUB"):
        self.capacity = capacity
        self.name = name
        self.currentAddress = currentAddress
        self.packages = []

    def addPackage(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            package.truck = "Delivered by: " + str(self.name)
            return True
        else:
            return False

    def removePackage(self, package):
        self.packages.remove(package)

    def setAddress(self, address):
        self.currentAddress = address

