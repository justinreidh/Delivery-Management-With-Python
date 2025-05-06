class Package:
    def __init__(self, packageID, address, deadline, city, zipCode, weight, note='', status="At hub", truck = ''):
        self.packageID = packageID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipCode = zipCode
        self.weight = weight
        self.note = note
        self.truck = truck
        self.status = status

    def __str__(self):
        #correctly print the package item
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.packageID, self.address, self.deadline, self.city, self.zipCode, self.weight, self.note, self.truck, self.status)

