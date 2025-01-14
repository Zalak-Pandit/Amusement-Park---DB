use project;

CREATE TABLE Visitor (
    VisitorID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    Phone VARCHAR(15),
    Email VARCHAR(100) UNIQUE,
    DateOfBirth DATE,
    MembershipStatus ENUM('Regular', 'Silver', 'Gold', 'Platinum') DEFAULT 'Regular'
);

CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Position VARCHAR(50),
    Phone VARCHAR(15),
    Email VARCHAR(100) UNIQUE,
    HireDate DATE,
    Salary DECIMAL(10,2)
);
INSERT INTO Employee (Name, Position, Phone, Email, HireDate, Salary)
VALUES ('Emily Davis', 'Customer Service Representative', '456-789-0123', 'emilydavis@example.com', '2024-01-05', 35000.00);
INSERT INTO Employee (Name, Position, Phone, Email, HireDate, Salary)
VALUES 
('Laura Martinez', 'Park Supervisor', '890-123-4567', 'lauramartinez@example.com', '2020-06-30', 55000.00),
('James Taylor', 'Electrician', '901-234-5678', 'jamestaylor@example.com', '2023-04-15', 44000.00);

CREATE TABLE Ride (
    RideID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Type VARCHAR(50),
    Capacity INT,
    OperatingStatus ENUM('Operating', 'Closed') DEFAULT 'Operating',
    MaintenanceDate DATE,
    EmployeeID INT,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);
INSERT INTO Ride (Name, Type, Capacity, OperatingStatus, MaintenanceDate, EmployeeID)
VALUES ('Ferris Wheel', 'Family', 40, 'Operating', '2024-11-25', 2);
INSERT INTO Ride (Name, Type, Capacity, OperatingStatus, MaintenanceDate, EmployeeID)
VALUES 
('Splash Adventure', 'Water Ride', 20, 'Operating', '2024-11-20', 2),
('Haunted Mansion', 'Dark Ride', 15, 'Closed', '2024-11-05', 2);
CREATE TABLE Ticket (
    TicketID INT PRIMARY KEY AUTO_INCREMENT,
    VisitorID INT,
    PurchaseDate DATE,
    Price DECIMAL(8,2),
    TicketType ENUM('Single-Day', 'Season Pass') DEFAULT 'Single-Day',
    FOREIGN KEY (VisitorID) REFERENCES Visitor(VisitorID)
);

CREATE TABLE Reservation (
    ReservationID INT PRIMARY KEY AUTO_INCREMENT,
    VisitorID INT,
    RideID INT,
    ReservationDate DATE,
    TimeSlot TIME,
    FOREIGN KEY (VisitorID) REFERENCES Visitor(VisitorID),
    FOREIGN KEY (RideID) REFERENCES Ride(RideID)
);

CREATE TABLE Payment (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    TicketID INT UNIQUE,
    Amount DECIMAL(8,2),
    PaymentDate DATE,
    PaymentMethod ENUM('Cash', 'Credit Card', 'Debit Card', 'Online') DEFAULT 'Credit Card',
    FOREIGN KEY (TicketID) REFERENCES Ticket(TicketID)
);

CREATE VIEW AvailableRidesView AS
SELECT RideID, Name, Type, Capacity, OperatingStatus
FROM Ride
WHERE OperatingStatus = 'Operating';

CREATE VIEW VisitorTicketHistoryView AS
SELECT V.Name AS VisitorName, T.TicketID, T.PurchaseDate, T.Price, T.TicketType
FROM Visitor V
JOIN Ticket T ON V.VisitorID = T.VisitorID;



DELIMITER //
CREATE PROCEDURE AddNewVisitor (
    IN p_Name VARCHAR(100),
    IN p_Address VARCHAR(255),
    IN p_Phone VARCHAR(15),
    IN p_Email VARCHAR(100),
    IN p_DateOfBirth DATE,
    IN p_MembershipStatus ENUM('Regular', 'Silver', 'Gold', 'Platinum')
)
BEGIN
    INSERT INTO Visitor (Name, Address, Phone, Email, DateOfBirth, MembershipStatus)
    VALUES (p_Name, p_Address, p_Phone, p_Email, p_DateOfBirth, p_MembershipStatus);
END //

DELIMITER;

DELIMITER //
CREATE PROCEDURE RecordTicketPurchase(
    IN p_VisitorID INT,
    IN p_PurchaseDate DATE,
    IN p_Price DECIMAL(8,2),
    IN p_TicketType ENUM('Single-Day', 'Season Pass')
)
BEGIN
    INSERT INTO Ticket (VisitorID, PurchaseDate, Price, TicketType)
    VALUES (p_VisitorID, p_PurchaseDate, p_Price, p_TicketType);
END //
DELIMITER ;

DELIMITER //

CREATE PROCEDURE ScheduleRideMaintenance(
    IN p_RideID INT,
    IN p_MaintenanceDate DATE
)
BEGIN
    UPDATE Ride
    SET OperatingStatus = 'Closed', MaintenanceDate = p_MaintenanceDate
    WHERE RideID = p_RideID;
END //

DELIMITER ;

DELIMITER //
CREATE TRIGGER AfterTicketInsert
AFTER INSERT ON Ticket
FOR EACH ROW
BEGIN
    INSERT INTO Payment (TicketID, Amount, PaymentDate, PaymentMethod)
    VALUES (NEW.TicketID, NEW.Price, NEW.PurchaseDate, 'Credit Card');
END //

DELIMITER //
CREATE TRIGGER BeforeReservationInsert
BEFORE INSERT ON Reservation
FOR EACH ROW
BEGIN
    DECLARE current_reservations INT;
    DECLARE ride_capacity INT;
    
    SELECT COUNT(*) INTO current_reservations
    FROM Reservation
    WHERE RideID = NEW.RideID AND ReservationDate = NEW.ReservationDate AND TimeSlot = NEW.TimeSlot;
    
    SELECT Capacity INTO ride_capacity
    FROM Ride
    WHERE RideID = NEW.RideID;
    
    IF current_reservations >= ride_capacity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ride capacity exceeded for the selected time slot.';
    END IF;
END //

select * from Visitor;


