from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'abc'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Zalak$16102005',
    'database': 'project'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_visitor', methods=['GET', 'POST'])
def add_visitor():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['address'],
            request.form['phone'],
            request.form['email'],
            request.form['dob'],
            request.form['membership_status']
        )
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.callproc('AddNewVisitor', data)
            conn.commit()
            flash('Visitor Added Successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('add_visitor'))
    return render_template('add_visitor.html')

@app.route('/purchase_ticket', methods=['GET', 'POST'])
def purchase_ticket():
    if request.method == 'POST':
        data = (
            request.form['visitor_id'],
            request.form['purchase_date'],
            request.form['price'],
            request.form['ticket_type']
        )
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.callproc('RecordTicketPurchase', data)

            conn.commit()

            flash('Ticket Purchased Successfully! Payment Recorded via Trigger.', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('purchase_ticket'))
    return render_template('purchase_ticket.html')


@app.route('/schedule_maintenance', methods=['GET', 'POST'])
def schedule_maintenance():
    if request.method == 'POST':
        ride_id = request.form['ride_id']
        maintenance_date = request.form['maintenance_date']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.callproc('ScheduleRideMaintenance', [ride_id, maintenance_date])
            conn.commit()
            flash('Ride maintenance scheduled successfully!', 'success')
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect('/schedule_maintenance')
    return render_template('schedule_maintenance.html')

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        data = (
            request.form['visitor_id'],
            request.form['ride_id'],
            request.form['reservation_date'],
            request.form['time_slot']
        )
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = """
                INSERT INTO Reservation (VisitorID, RideID, ReservationDate, TimeSlot)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, data)
            conn.commit()

            flash('Reservation made successfully!', 'success')
        except mysql.connector.Error as err:
            if err.errno == 1644:  # Custom trigger error
                flash(f'Error: {err.msg}', 'danger')
            else:
                flash(f'Database Error: {err}', 'danger')
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('make_reservation'))
    return render_template('make_reservation.html')

@app.route('/available_rides')
def available_rides():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM AvailableRidesView")
        rides = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f'Database Error: {err}', 'danger')
        rides = []
    finally:
        cursor.close()
        conn.close()
    return render_template('available_rides.html', rides=rides)

@app.route('/visitor_ticket_history')
def visitor_ticket_history():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM VisitorTicketHistoryView")
        tickets = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f'Database Error: {err}', 'danger')
        tickets = []
    finally:
        cursor.close()
        conn.close()
    return render_template('visitor_ticket_history.html', tickets=tickets)


if __name__ == '__main__':
    app.run(debug=True)
