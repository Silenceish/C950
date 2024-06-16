import re
from datetime import datetime

class Package:

    def __init__(self, ID, destination, city, state, zip, deadline,
                 weight, notes, status):
        self.ID = ID
        self.destination = destination
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.time_delivered = None



    def __str__(self):
        return f"{self.ID}, {self.destination}, {self.city}, {self.state}, {self.zip}, {self.deadline}," \
               f"{self.weight}, {self.notes}, {self.status}, {self.time_delivered}"

    # Change status of individual package
    def change_status(self, status):
        self.status = status


    # Returns value of specified truck
    def specific_truck(self, package):
        note = package.notes
        return int(note[len(note) - 1])

    # Returns list of packages to be grouped together
    def group_packages(self, package):
        note = package.notes
        # Pull integer values from status string
        packages = re.findall('\d+', note)
        for i in range(0, len(packages)):
            packages[i] = int(packages[i])
        packages.append(package.ID)
        # Return list containing packages that must be grouped
        return packages

    # Get correct address for package
    def wrong_address(self, package, new_address):
        split_address = new_address.split(",")
        package.destination = split_address[0]
        package.city = split_address[1]
        package.state = split_address[2]
        package.zip = split_address[3]

    # Get arrival time for delayed packages
    def delayed_package(self, package):
        note = package.notes
        # Pull time value from status string
        arrival_time = datetime.strptime(note, '%I:%M %p')
        return arrival_time

