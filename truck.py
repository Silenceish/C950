from datetime import timedelta

class Truck:
    AVERAGE_SPEED = 18
    MAX_PACKAGES = 16

    def __init__(self, truck_ID, mph=AVERAGE_SPEED, size=MAX_PACKAGES):
        self.ID = truck_ID
        self.mph = mph
        self.max_size = size
        self.package_list = []
        self.total_distance = 0.0
        self.time = timedelta(hours=8, minutes=0, seconds=0)
        self.driver = None
        self.location = "4001 South 700 East"
        self.timestamps = []

    # Add package if truck isn't full
    def add_package(self, package):
        if self.is_full():
            return False
        else:
            self.package_list.append(package.ID)
            return True

    # Update package status to show it is en route
    def packages_on_truck(self, ht):
        for package_ID in self.package_list:
            package = ht.lookup_package(package_ID)
            package.change_status(f"On truck {self.ID}")

    # Change package status to delivered and update the time delivered
    def package_delivered(self, ht, pID):
        package = ht.lookup_package(pID)
        package.change_status("Delivered")
        package.time_delivered = self.time

    # Update truck mileage traveled
    def add_mileage(self, miles):
        self.total_distance += miles

    # Checks if truck is full
    def is_full(self):
        if len(self.package_list) == self.max_size:
            return True
        return False


    # Delivers next closest package and updates all values
    def deliver_packages(self, ht, address_list, distance_list):
        end_x = 0
        while len(self.package_list) > 0:
            y = address_list.index(self.location)
            min_distance = 5000
            min_id = len(self.package_list) + 1
            for packages in self.package_list:
                package = ht.lookup_package(packages)
                x = address_list.index(package.destination)
                distance = distance_list[x][y]
                # Convert string from grid to float value, flips x,y if needed
                try:
                    distance = float(distance)
                except: pass
                try:
                    distance = float(distance_list[y][x])
                except:pass

                # Finds the closest package to current location
                if distance < min_distance:
                    min_distance = distance
                    min_id = package.ID
                    end_x = x
            # Moves truck to location and delivers package
            next_package = ht.lookup_package(min_id)
            self.location = next_package.destination
            self.total_distance += min_distance
            self.time += timedelta(minutes=(min_distance / self.mph * 60))
            # Track location of truck using timestamps and location
            self.timestamps.append((self.time, self.location))
            next_package.time_delivered = self.time
            self.package_delivered(ht, next_package.ID)
            self.package_list.pop(self.package_list.index(min_id))
        # Send truck back to hub
        self.go_home(float(distance_list[end_x][0]))

    def go_home(self, distance):
        self.location = "4001 South 700 East"
        self.total_distance += distance
        self.time += timedelta(minutes=(distance / self.mph * 60))
        self.timestamps.append((self.time, self.location))
        self.remove_driver()

    def add_driver(self, driver):
        self.driver = driver

    def remove_driver(self):
        self.driver = None

