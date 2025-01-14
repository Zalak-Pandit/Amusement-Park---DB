from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure Database URI: Replace with your actual database credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/amusement_park_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models
from models import Visitor, Employee, Ride, Ticket, Reservation, Payment

@app.route('/')
def index():
    rides = Ride.query.filter_by(OperatingStatus='Operating').all()
    return render_template('index.html', rides=rides)

@app.route('/add_visitor', methods=['GET', 'POST'])
def add_visitor():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        dob = request.form['dob']
        membership = request.form['membership']
        
        new_visitor = Visitor(
            Name=name,
            Address=address,
            Phone=phone,
            Email=email,
            DateOfBirth=datetime.strptime(dob, '%Y-%m-%d'),
            MembershipStatus=membership
        )
        try:
            db.session.add(new_visitor)
            db.session.commit()
            flash('Visitor added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding visitor: {e}', 'danger')
            return redirect(url_for('add_visitor'))
    return render_template('add_visitor.html')

@app.route('/view_rides')
def view_rides():
    rides = db.session.execute('SELECT * FROM AvailableRidesView').fetchall()
    return render_template('view_rides.html', rides=rides)

# Additional routes for booking tickets, making reservations, etc.

if __name__ == '__main__':
    app.run(debug=True)
