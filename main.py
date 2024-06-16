# Tony Liebes - Student ID: 010532106

import csv
from datetime import timedelta, datetime

from hashtable import HashTable
from package import Package
from truck import Truck

NUM_DRIVERS = 2
NUM_TRUCKS = 3


def get_package_info(ht):
    id_list = []
    with open('CSV/packages.csv') as packages:
        packageInfo = csv.reader(packages, delimiter=',')
        for package in packageInfo:
            ID = int(package[0])
            destination = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deadline = package[5]
            weight = package[6]
            notes = package[7]
            status = "At Hub"

            new_Package = Package(ID, destination, city, state, zip, deadline, weight, notes, status)
            id_list.append(ID)

            ht.insert(ID, new_Package)
    return id_list


# Read addresses into a list
def get_addresses():
    address_list = []
    with open('CSV/addresses.csv') as addresses:
        read_address = csv.reader(addresses)
        for address in read_address:
            # Pull string from created list and split off the street address
            split = address[0].split('\n')
            street_address = split[1]
            street_address = street_address[1:]
            address_list.append(street_address)
    return address_list


# Unsorted assignment of packages to trucks
def assign_to_truck(truck_list, ht, pIDs):
    packages_without_restrictions = []
    for id in pIDs:
        package = ht.lookup_package(id)
        # Check if package exists
        if package is not None:
            # Check if package has already been assigned
            already_assigned = False
            for truck in truck_list:
                if id in truck.package_list:
                    already_assigned = True
            if not already_assigned:
                # Handle packages with notes
                if len(package.notes) > 0:
                    if "Can only be on" in package.notes:
                        assigned_truck = package.specific_truck(package)
                        add_to_truck(truck_list[assigned_truck - 1], package)
                    elif "Delayed" in package.notes:
                        if "EOD" in package.deadline:
                            add_to_truck(truck_list[2], package)
                        else:
                            add_to_truck(truck_list[1], package)
                    elif "Must be delivered with" in package.notes:
                        grouped = package.group_packages(package)
                        for item in grouped:
                            if item not in truck_list[0].package_list:
                                package = ht.lookup_package(item)
                                add_to_truck(truck_list[0], package)
                    elif "Wrong address" in package.notes:
                        package.wrong_address(package, "410 S State St, Salt Lake City, UT, 84111")
                        add_to_truck(truck_list[2], package)
                    elif "load last" in package.notes:
                        for i in range(0, len(truck_list)):
                            if add_to_truck(truck_list[i], package):
                                break

                elif package.deadline != "EOD":
                    for i in range(len(truck_list)):
                        if add_to_truck(truck_list[i], package):
                            break
                # I'm sure there's a better way to do this
                # Adds special note to packages without restrictions
                else:
                    packages_without_restrictions.append(id)
                    package.notes = "load last"
    # Recursively call assign_to_truck function using list of non-restricted packages
    if len(packages_without_restrictions) > 0:
        assign_to_truck(truck_list, ht, packages_without_restrictions)


def add_to_truck(truck, package):
    success = truck.add_package(package)
    return success


# Read distances into matrix
def distance_matrix(address_list):
    with open('CSV/distances.csv') as distances:
        distance_line = csv.reader(distances)
        # Add each list from reader into new list to create matrix
        distance_line = list(distance_line)
    return distance_line


def main():
    package_ht = HashTable()
    package_ids = get_package_info(package_ht)
    address_list = get_addresses()
    distances = distance_matrix(address_list)
    truck_list = []
    driver_list = []

    # Create trucks and drivers using iteration for maintainability
    for i in range(1, NUM_TRUCKS + 1):
        new_truck = Truck(i)
        truck_list.append(new_truck)

    for i in range(1, NUM_DRIVERS + 1):
        driver_list.append(i)

    # Assign drivers to trucks
    assign_to_truck(truck_list, package_ht, package_ids)
    for i in range(len(driver_list)):
        truck_list[i].add_driver(driver_list[i])

    # Create variables for trucks
    # Unclean code but simpler for now
    truck_one = truck_list[0]
    truck_two = truck_list[1]
    truck_three = truck_list[2]

    # Load truck one
    truck_one.packages_on_truck(package_ht)
    truck_one.timestamps.append((truck_one.time, truck_one.location))
    # Sends out truck one
    truck_one.deliver_packages(package_ht, address_list, distances)

    # Sets truck two time for late arrivals
    truck_two.time = timedelta(hours=9, minutes=5, seconds=0)
    # Load and send out truck two
    truck_two.packages_on_truck(package_ht)
    truck_two.timestamps.append((truck_two.time, truck_two.location))
    truck_two.deliver_packages(package_ht,address_list, distances)

    # Sets truck three time for when truck one returns
    truck_three.time = truck_one.time
    # Remove driver from truck one and put on truck 3
    truck_one.remove_driver()
    truck_three.add_driver(1)
    # Load truck three
    truck_three.packages_on_truck(package_ht)
    truck_three.timestamps.append((truck_three.time, truck_three.location))
    # Send out truck three
    truck_three.deliver_packages(package_ht, address_list, distances)

    total_miles = truck_one.total_distance + truck_two.total_distance + truck_three.total_distance

    # for tup in truck_one.timestamps:
    #     print(f"{tup[0]} at {tup[1]}")
    run = True

    print("WGU UPS Truck\n\n")
    while run:
        for truck in truck_list:
            if len(truck.package_list) == 0 and truck.driver is not None:

        print("What time would you like to see?")
        print("Enter in form HH:MM:SS")
        # Convert time input to datetime and then timedelta for comparison
        input_time = input("Please enter a time later than 08:00:00\n")
        time_input = datetime.strptime(input_time, "%H:%M:%S")
        time_input = timedelta(hours=time_input.hour, minutes=time_input.minute, seconds=time_input.second)

        # Show location of truck at desired time
        for truck in truck_list:
            closest_time = truck.timestamps[0][0]
            timestamp_index = 0
            for time in truck.timestamps:
                # Find nearest timestamp to desired time
                if time_input > time[0] > closest_time:
                    closest_time = time[0]
                    timestamp_index = truck.timestamps.index(time)
            print(f"At {time_input} Truck {truck.ID} was at {truck.timestamps[timestamp_index][1]} ")












if __name__ == "__main__":
    main()
