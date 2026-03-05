CREATE DATABASE slot_booking;

USE slot_booking;

CREATE TABLE slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slot_time VARCHAR(50),
    status VARCHAR(20)
);

INSERT INTO slots (slot_time, status) VALUES
('10:00 AM', 'Available'),
('11:00 AM', 'Available'),
('12:00 PM', 'Available'),
('01:00 PM', 'Available');