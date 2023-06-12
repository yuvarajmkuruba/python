from pymongo import MongoClient
import datetime

# Connect to the MongoDB server
client = MongoClient("mongodb+srv://yuvarajmkuruba:uv12345@pyproject.p2hdw2g.mongodb.net/?retryWrites=true&w=majority")

# Create a database
db = client['car_rental_db']

# Create a collection
collection = db['cars']

def create_car(car_data, time_spec):
    # Add a new car document with a time specification
    car_data['time_spec'] = time_spec
    collection.insert_one(car_data)
    print('Car created successfully!')

def get_car(car_id):
    # Find a car document based on ID
    car = collection.find_one({'_id': car_id})
    if car:
        return car
    else:
        return None

def update_car(car_id, updated_data):
    # Update a car document
    collection.update_one({'_id': car_id}, {'$set': updated_data})
    print('Car updated successfully!')

def delete_car(car_id):
    # Delete a car document
    collection.delete_one({'_id': car_id})
    print('Car deleted successfully!')

def rent_car(car_id, customer_name, rental_duration, driver_details):
    car = get_car(car_id)
    if car:
        if car['available']:
            car['available'] = False
            car['rented_by'] = customer_name
            car['return_date'] = datetime.datetime.now() + datetime.timedelta(days=rental_duration)
            car['driver_details'] = driver_details
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
            car['driver_details'] = None
            update_car(car_id, car)
            print('Car returned successfully!')
        else:
            print('Car is already available.')
    else:
        print('Car not found.')

def delete_all_reservations():
    # Delete all car documents with 'available' set to False
    collection.delete_many({'available': False})
    print('All reservations deleted successfully!')

def view_reservations():
    reservations = collection.find({'available': False})
    for car in reservations:
        return_date = car['return_date'].strftime('%Y-%m-%d') if car['return_date'] else 'N/A'
        driver_details = car['driver_details'] if car.get('driver_details') else 'N/A'
        print(f"Car ID: {car['_id']}, Model: {car['model']}, Booked by: {car['rented_by']}, Return Date: {return_date}, Driver Details: {driver_details}")

# Main program
if __name__ == '__main__':
    while True:
        print('1. Add Car')
        print('2. Rent Car')
        print('3. View Reservations')
        print('4. Delete Booked Car')
        print('5. Return Car')
        print('6. Delete All Reservations')
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
            driver_name = input('Enter Driver Name: ')
            license_number = input('Enter Driver License Number: ')
            contact_number = input('Enter Driver Contact Number: ')
            driver_details = {
                'name': driver_name,
                'license_number': license_number,
                'contact_number': contact_number
            }
            rent_car(car_id, customer_name, rental_duration, driver_details)
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

        elif choice == 0:
            break

        else:
            print('Invalid choice. Please try again.')
            print()
