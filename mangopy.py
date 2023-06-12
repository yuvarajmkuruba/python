# mongodb+srv://myAtlasDBUser:Uv@12345@myatlasclusteredu.c4qedue.mongodb.net/
import pymongo
from pymongo import MongoClient
# from task import update_available_tickets
# Connect to the MongoDB server
client = MongoClient("mongodb+srv://yuvarajmkuruba:uv12345@pyproject.p2hdw2g.mongodb.net/?retryWrites=true&w=majority")
# Access the reservations database
db = client['reservations']
# Access the reservations collectionmongodb+srv://myAtlasDBUser:Uv@12345@myatlasclusteredu.c4qedue.mongodb.net/
collection = db['reservations']
def add_reservation(name, email, tickets, from_place, to_place, date):
    # Check if there are enough available tickets
    available_tickets = get_available_tickets()
    if tickets > available_tickets:
        print("Not enough available tickets.")
        return
    
    # Create the reservation document
    reservation = {
        'name': name,
        'email': email,
        'tickets': tickets,
        'from_place': from_place,
        'to_place': to_place,
        'created_at': date
    }
    
    # Add the reservation to the collection
    collection.insert_one(reservation)
    
    # Update the number of available tickets
    # update_available_tickets(available_tickets - tickets)
    
    print("Reservation added successfully.")


def edit_reservation(reservation_id, name, email, tickets, from_place, to_place):
    # Check if the reservation exists
    reservation = collection.find_one({'_id': reservation_id})
    if reservation is None:
        print("Reservation not found.")
        return
    
    # Get the previous number of tickets
    previous_tickets = reservation['tickets']
    
    # Update the reservation details in the collection
    collection.update_one(
        {'_id': reservation_id},
        {'$set': {
            'name': name,
            'email': email,
            'tickets': tickets,
            'from_place': from_place,
            'to_place': to_place
        }}
    )
    # Update the number of available tickets
    # update_available_tickets(get_available_tickets() + previous_tickets - tickets)
    print("Reservation updated successfully.")
def view_tickets_booked():
    tickets_booked = collection.count_documents({})
    print(f"Total tickets booked: {tickets_booked}")


def delete_all_data():
    collection.delete_many({})
    # update_available_tickets(0)
    print("All data deleted.")


def get_available_tickets():
    tickets_booked = collection.aggregate([{'$group': {'_id': None, 'total_tickets': {'$sum': '$tickets'}}}])
    tickets_booked = next(tickets_booked, {'total_tickets': 0})['total_tickets']
    available_tickets = 100 - tickets_booked
    return available_tickets


def get_all_reservations(sort_by=None, date=None):
    query = {}
    if date is not None:
        query['created_at'] = date
    
    sort_key = 'created_at' if sort_by is None else sort_by
    reservations = collection.find(query).sort(sort_key)
    return list(reservations)


def show_menu():
    print("==== Reservation Booking System ====")
    print("1. Add Reservation")
    print("2. Edit Reservation")
    print("3. View Tickets Booked")
    print("4. View All Reservations")
    print("5. Delete All Data")
    print("6. Quit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            name = input("Enter the name: ")
            email = input("Enter the email: ")
            tickets = int(input("Enter the number of tickets: "))
            from_place = input("Enter the from place: ")
            to_place = input("Enter the to place: ")
            date = input("Enter the date (YYYY-MM-DD): ")
            add_reservation(name, email, tickets, from_place, to_place, date)
        
        elif choice == '2':
            reservation_id = input("Enter the reservation ID: ")
            name = input("Enter the new name: ")
            email = input("Enter the new email: ")
            tickets = int(input("Enter the new number of tickets: "))
            from_place = input("Enter the new from place: ")
            to_place = input("Enter the new to place: ")
            edit_reservation(reservation_id, name, email, tickets, from_place, to_place)
        
        elif choice == '3':
            view_tickets_booked()
        
        elif choice == '4':
            date = input("Enter the date (YYYY-MM-DD): ")
            reservations = get_all_reservations(sort_by='created_at', date=date)
            if not reservations:
                print("No reservations found.")
            else:
                print("==== All Reservations ====")
                for reservation in reservations:
                    print(f"ID: {reservation['_id']}, Name: {reservation['name']}, Email: {reservation['email']}, Tickets: {reservation['tickets']}, From: {reservation['from_place']}, To: {reservation['to_place']}, Created At: {reservation['created_at']}")
        
        elif choice == '5':
            delete_all_data()
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice. Please try again.")
if __name__ == '__main__':
    main()
# Close the connection
client.close()