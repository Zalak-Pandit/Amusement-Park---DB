import mysql.connector


connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Zalak$16102005',
    database='project'
)

cursor = connection.cursor()


def add_visitor():
    Name = input("Enter Visitor name: ")
    Address = (input("Enter visitor age: "))
    Phone = (input("Enter contact number: "))
    Email = input("Enter Visitor name: ")
    DateofBirth = input ("Enter DOB: ")
    query = "INSERT INTO Visitor (Name, Address, Phone, Email, DateofBirth) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (Name, Address, Phone,Email, DateofBirth))
    connection.commit()
    print("Visitor added successfully.")

def view_visitors():
    cursor.execute("SELECT * FROM Visitor")
    for row in cursor.fetchall():
        print(row)

def update_visitor():
    visitor_id = int(input("Enter visitor ID to update: "))
    new_contact = input("Enter new contact number: ")
    query = "UPDATE visitors SET phone = %s WHERE VisitorID  = %s"
    cursor.execute(query, (new_contact, visitor_id))
    connection.commit()
    print("Visitor updated successfully.")

def delete_visitor():
    visitor_id = int(input("Enter visitor ID to delete: "))
    query = "DELETE FROM Visitor WHERE VisitorID = %s"
    cursor.execute(query, (visitor_id,))
    connection.commit()
    print("Visitor deleted successfully.")


def add_ride():
    Name = input("Enter ride name: ")
    Type = input("Enter type of ride: ")
    Capacity = input ("Enter capacity: ")
    OperatingStatus = input("Enter ride status (Operating/Closed): ")
    Date = input("Enter Maintainance Date: ")
    EmployeeID = int(input("Enter EmployeeID: "))
    query = "INSERT INTO Ride (Name,Type,Capacity, OperatingStatus, Date, EmployeeID) VALUES (%s, %s, %s, %s, %s, %d)"
    cursor.execute(query, (Name, Type, Capacity, OperatingStatus, Date, EmployeeID))
    connection.commit()
    print("Ride added successfully.")

def view_rides():
    cursor.execute("SELECT * FROM Ride")
    for row in cursor.fetchall():
        print(row)

def update_ride_status():
    RideID = int(input("Enter ride ID to update status: "))
    new_status = input("Enter new status (Operating/Closed): ")
    query = "UPDATE Ride SET OperatingStatus = %s WHERE RideID = %s"
    cursor.execute(query, (new_status, RideID))
    connection.commit()
    print("Ride status updated successfully.")

def delete_ride():
    RideID = int(input("Enter ride ID to delete: "))
    query = "DELETE FROM Ride WHERE RideID = %s"
    cursor.execute(query, (RideID,))
    connection.commit()
    print("Ride deleted successfully.")


def add_reservation():
    VisitorID = int(input("Enter visitor ID: "))
    RideID = int(input("Enter ride ID: "))
    ReservationDate = int(input("Enter Date (YYYY-MM-DD)"))
    TimeSlot = input("Enter reservation time (HH:MM:SS): ")
    query = "INSERT INTO Reservation (VisitorID, RideID,ReservationDate, TimeSlot) VALUES (%d, %d,%s, %s)"
    cursor.execute(query, (VisitorID, RideID,ReservationDate, TimeSlot))
    connection.commit()
    print("Reservation made successfully.")

def view_reservations():
    cursor.execute("SELECT * FROM Reservation")
    for row in cursor.fetchall():
        print(row)

def delete_reservation():
    reservation_id = int(input("Enter Reservation ID to delete: "))
    query = "DELETE FROM Reservation WHERE id = %s"
    cursor.execute(query, (reservation_id,))
    connection.commit()
    print("Reservation deleted successfully.")


def add_payment():
    visitor_id = int(input("Enter visitor ID: "))
    amount = float(input("Enter payment amount: "))
    payment_date = input("Enter payment date (YYYY-MM-DD): ")
    query = "INSERT INTO payments (visitor_id, amount, payment_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (visitor_id, amount, payment_date))
    connection.commit()
    print("Payment recorded successfully.")

def view_payments():
    cursor.execute("SELECT * FROM payments")
    for row in cursor.fetchall():
        print(row)


def main_menu():
    while True:
        print("\n--- Amusement Park Management ---")
        print("1. Add Visitor")
        print("2. View Visitors")
        print("3. Update Visitor")
        print("4. Delete Visitor")
        print("5. Add Ride")
        print("6. View Rides")
        print("7. Update Ride Status")
        print("8. Delete Ride")
        print("9. Make Reservation")
        print("10. View Reservations")
        print("11. Cancel Reservation")
        print("12. Record Payment")
        print("13. View Payments")
        print("14. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_visitor()
        elif choice == '2':
            view_visitors()
        elif choice == '3':
            update_visitor()
        elif choice == '4':
            delete_visitor()
        elif choice == '5':
            add_ride()
        elif choice == '6':
            view_rides()
        elif choice == '7':
            update_ride_status()
        elif choice == '8':
            delete_ride()
        elif choice == '9':
            add_reservation()
        elif choice == '10':
            view_reservations()
        elif choice == '11':
            delete_reservation()
        elif choice == '12':
            add_payment()
        elif choice == '13':
            view_payments()
        elif choice == '14':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")


main_menu()

cursor.close()
connection.close()
