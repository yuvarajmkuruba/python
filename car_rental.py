from pymongo import MongoClient
import datetime
import time
# Connect to the MongoDB server
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient("mongodb+srv://yuvarajmkuruba:uv12345@pyproject.p2hdw2g.mongodb.net/?retryWrites=true&w=majority")


# Create a database
db = client['car_rental_db']

# Create collections
cars_collection = db['cars']
drivers_collection = db['drivers']
def view_driver(driver_id):
    driver = get_driver(driver_id)
    if driver:
        print(f"Driver ID: {driver['_id']}")
        print(f"Name: {driver['name']}")
        print(f"License Number: {driver['license_number']}")
        print(f"Contact Number: {driver['contact_number']}")
    else:
        print('Driver not found.')

def create_car(car_data, time_spec):
    # Add a new car document with a time specification
    car_data['time_spec'] = time_spec
    cars_collection.insert_one(car_data)
    print('Car created successfully!')

def get_car(car_id):
    # Find a car document based on ID
    car = cars_collection.find_one({'_id': car_id})
    if car:
        return car
    else:
        return None

def update_car(car_id, updated_data):
    # Update a car document
    cars_collection.update_one({'_id': car_id}, {'$set': updated_data})
    print('Car updated successfully!')

def delete_car(car_id):
    # Delete a car document
    cars_collection.delete_one({'_id': car_id})
    print('Car deleted successfully!')

def rent_car(car_id, customer_name, rental_duration, driver_id):
    car = get_car(car_id)
    if car:
        if car['available']:
            car['available'] = False
            car['rented_by'] = customer_name
            car['return_date'] = datetime.datetime.now() + datetime.timedelta(days=rental_duration)
            car['driver_id'] = driver_id
            update_car(car_id, car)
            print('Car rented successfully!')
        else:
            print('Car is not available for rent.')
    else:
        print('Car not found.')

def return_car(car_id):
    car = get_car(car_id)
    if car:
        if not car['available']:
            car['available'] = True
            car['rented_by'] = None
            car['return_date'] = None
            car['driver_id'] = None
            update_car(car_id, car)
            print('Car returned successfully!')
        else:
            print('Car is already available.')
    else:
        print('Car not found.')

def delete_all_reservations():
    # Delete all car documents with 'available' set to False
    cars_collection.delete_many({'available': False})
    print('All reservations deleted successfully!')

def view_reservations():
    reservations = cars_collection.find({'available': False})
    for car in reservations:
        return_date = car['return_date'].strftime('%Y-%m-%d') if car['return_date'] else 'N/A'
        driver_name = get_driver_name(car['driver_id'])
        print(f"Car ID: {car['_id']}, Model: {car['model']}, Booked by: {car['rented_by']}, Return Date: {return_date}, Driver: {driver_name}")

def create_driver(driver_data):
    # Add a new driver document
    drivers_collection.insert_one(driver_data)
    print('Driver created successfully!')

def get_driver(driver_id):
    # Find a driver document based on ID
    driver = drivers_collection.find_one({'_id': driver_id})
    if driver:
        return driver
    else:
        return None
print("hii")
def get_driver_name(driver_id):
    # Get the driver name based on ID
    driver = get_driver(driver_id)
    if driver:
        return driver['name']
    else:
        return 'N/A'
def view_driver():
    drivers = drivers_collection.find()
    for driver in drivers:
        print(f"Driver ID: {driver['_id']}")
        print(f"Name: {driver['name']}")
        print(f"License Number: {driver['license_number']}")
        print(f"Contact Number: {driver['contact_number']}")
        print()
# Main program
if __name__ == '__main__':
    while True:
        time.sleep(5)
        print('1. Add Car')
        print('2. Rent Car')
        print('3. View Reservations')
        print('4. Delete Booked Car')
        print('5. Return Car')
        print('6. Delete All Reservations')
        print('7. Add Driver')
        print('8. View Driver')
        print('9. View All Drivers')
        print('0. Exit')
        
        choice = int(input('Enter your choice: '))

        if choice == 1:
            car_id = input('Enter Car ID: ')
            model = input('Enter Car Model: ')
            car_data = {
                '_id': car_id,
                'model': model,
                'available': True,
                'rented_by': None
            }
            time_spec = int(input('Enter Time Specification (in days): '))
            create_car(car_data, time_spec)
            print()

        elif choice == 2:
            car_id = input('Enter Car ID: ')
            customer_name = input('Enter Customer Name: ')
            rental_duration = int(input('Enter Rental Duration (in days): '))
            driver_id = input('Enter Driver ID: ')
            rent_car(car_id, customer_name, rental_duration, driver_id)
            print()

        elif choice == 3:
            view_reservations()
            print()

        elif choice == 4:
            car_id = input('Enter Car ID: ')
            delete_car(car_id)
            print()

        elif choice == 5:
            car_id = input('Enter Car ID: ')
            return_car(car_id)
            print()

        elif choice == 6:
            delete_all_reservations()
            print()

        elif choice == 7:
            driver_id = input('Enter Driver ID: ')
            driver_name = input('Enter Driver Name: ')
            driver_license = input('Enter Driver License Number: ')
            driver_contact = input('Enter Driver Contact Number: ')
            driver_data = {
                '_id': driver_id,
                'name': driver_name,
                'license_number': driver_license,
                'contact_number': driver_contact
            }
            create_driver(driver_data)
            print()
        elif choice == 8:
            driver_id = input('Enter Driver ID: ')
            view_driver(driver_id)
            print()

        elif choice == 9:
            view_driver()
            print()

        elif choice == 0:
            break

        else:
            print('Invalid choice. Please try again.')
            print()