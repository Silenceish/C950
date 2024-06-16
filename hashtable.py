class HashTable:
    def __init__(self):
        # Initialize hash table with 40 empty buckets
        self.size = 40;
        self.list = []
        for i in range(self.size):
            self.list.append([])

    # method to create hash value
    def get_hash(self, key):
        return hash(key) % len(self.list)

    # Adds new item to hash table
    def insert(self, key, value):
        kh = self.get_hash(key)
        bucket_list = self.list[kh]

        # Check if item already exists and update it
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = value
                return True

        # Add new item new bucket
        kv = [key, value]
        bucket_list.append(kv)
        return True

    # Retrieve item from hash table
    def lookup_package(self, key):
        kh = self.get_hash(key)
        bucket_list = self.list[kh]
        # Retrieve item if bucket is not empty and the key exists
        for item in bucket_list:
            if key == item[0]:
                return item[1]
        return None

    # Deletes item from hash table
    def delete_bucket(self, key):
        kh = self.get_hash(key)

        bucket_list = self.list[kh]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv[0], kv[1])

    def get_size(self):
        return self.size


    def print(self):
        for item in self.list:
            if item is not None:
                print(item[0][1])

