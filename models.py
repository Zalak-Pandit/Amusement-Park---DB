from app import db

class Visitor(db.Model):
    __tablename__ = 'Visitor'
    VisitorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Address = db.Column(db.String(255))
    Phone = db.Column(db.String(15))
    Email = db.Column(db.String(100), unique=True)
    DateOfBirth = db.Column(db.Date)
    MembershipStatus = db.Column(db.Enum('Regular', 'Silver', 'Gold', 'Platinum'), default='Regular')
    tickets = db.relationship('Ticket', backref='visitor', lazy=True)
    reservations = db.relationship('Reservation', backref='visitor', lazy=True)

class Employee(db.Model):
    __tablename__ = 'Employee'
    EmployeeID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Position = db.Column(db.String(50))
    Phone = db.Column(db.String(15))
    Email = db.Column(db.String(100), unique=True)
    HireDate = db.Column(db.Date)
    Salary = db.Column(db.Numeric(10,2))
    rides = db.relationship('Ride', backref='employee', lazy=True)

class Ride(db.Model):
    __tablename__ = 'Ride'
    RideID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Type = db.Column(db.String(50))
    Capacity = db.Column(db.Integer)
    OperatingStatus = db.Column(db.Enum('Operating', 'Closed'), default='Operating')
    MaintenanceDate = db.Column(db.Date)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('Employee.EmployeeID'))
    reservations = db.relationship('Reservation', backref='ride', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'Ticket'
    TicketID = db.Column(db.Integer, primary_key=True)
    VisitorID = db.Column(db.Integer, db.ForeignKey('Visitor.VisitiorID'))
    PurchaseDate = db.Column(db.Date)
    Price = db.Column(db.Numeric(8,2))
    TicketType = db.Column(db.Enum('Single-Day', 'Season Pass'), default='Single-Day')
    payment = db.relationship('Payment', backref='ticket', uselist=False)

class Reservation(db.Model):
    __tablename__ = 'Reservation'
    ReservationID = db.Column(db.Integer, primary_key=True)
    VisitorID = db.Column(db.Integer, db.ForeignKey('Visitor.VisitiorID'))
    RideID = db.Column(db.Integer, db.ForeignKey('Ride.RideID'))
    ReservationDate = db.Column(db.Date)
    TimeSlot = db.Column(db.Time)

class Payment(db.Model):
    __tablename__ = 'Payment'
    PaymentID = db.Column(db.Integer, primary_key=True)
    TicketID = db.Column(db.Integer, db.ForeignKey('Ticket.TicketID'), unique=True)
    Amount = db.Column(db.Numeric(8,2))
    PaymentDate = db.Column(db.Date)
    PaymentMethod = db.Column(db.Enum('Cash', 'Credit Card', 'Debit Card', 'Online'), default='Credit Card')
