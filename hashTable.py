class ChainingHashTable:
    #constructor with initial capacity
    def __init__(self, capacity=40):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    def insert(self, key, item):
        #get the bucket where the package will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #if the package already exists, update it
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        #add the package to the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #if the key value exists, return the package. If not, return None
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

