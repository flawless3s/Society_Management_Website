create database mysociety_4;
use mysociety_4;
show tables;

Create table role(
	role_id int(1) primary key not null,
    role_name char(10) not null
);
Insert Into role values(1,'Admin');
Insert Into role values(2,'Secretary');
Insert Into role values(3,'Treasurer');
Insert Into role values(4,'Member');
Insert Into role values(5,'Security');
select * from role;

CREATE TABLE Society_Detail (
	sid INT(5) PRIMARY KEY auto_increment,
    s_name CHAR(50) NOT NULL,
    s_address CHAR(70) NOT NULL,
    area VARCHAR(10) NOT NULL,
    city CHAR(20) NOT NULL,
    state CHAR(20) NOT NULL,
    country CHAR(15) DEFAULT 'india' NOT NULL,
    
    build_name VARCHAR(50),
    build_no varchar(10),	
    company_name VARCHAR(50),
    total_flats INT(5) NOT NULL,
    total_wing INT(5) NOT NULL,
    total_floor INT(5) NOT NULL,
    empty_flat INT(5) NOT NULL,
    no_of_flat_on_each_floor INT(5) NOT NULL
);
SELECT sid, CONCAT(s_name, ' - ', city, ', ', state) AS society_info 
FROM Society_Detail;
desc Society_Detail;

select * from Society_detail;
alter table Society_detail modify column s_address CHAR(70) NOT NULL;
ALTER TABLE Society_detail DROP INDEX s_address_unique_index;

SELECT INDEX_NAME, COLUMN_NAME
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'my_society_4'
  AND TABLE_NAME = 'Society_detail'
  AND NON_UNIQUE = 0;

INSERT INTO Society_Detail (s_name, s_address, area, city, state, country, build_name, build_no, company_name, total_flats, total_wing, total_floor, empty_flat, no_of_flat_on_each_floor)
VALUES
('Green Meadows', '123 Green Street', 'Urban', 'Mumbai', 'Maharashtra', 'india', 'Pintya shetty', 1357908642, 'Green Corp', 88, 2, 15, 10, 3);

CREATE TABLE Users(
	id int(10) primary key auto_increment,
	sid INT(5),
    role_id int(1) not null,
    uid VARCHAR(50) UNIQUE not null,
    name CHAR(50) not null,
	email VARCHAR(50) NOT null,
    phone varchar(10) NOT NULL,
    photo_link Varchar(200),
    admin_approval BOOLEAN not null default 0,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approval_date date,
    is_active BOOLEAN not null default 1,
    
	
    foreign key (role_id) references role(role_id),
    foreign key (sid) references Society_Detail(sid)
);

INSERT INTO Users (sid, role_id, uid, name, email, phone, photo_link, admin_approval, registration_date, approval_date, is_active)
VALUES
(null, 1, 'user1', 'John Doe', 'john.doe@example.com', 1234567890, 'https://drive.google.com/file/d/1Lk_KFfmubXWdNpm_Cj1XRljBoh_HYU_K/view?usp=drive_link', 1, '2024-06-13', '2024-06-13', 1),
(1, 2, 'user2', 'Jane Smith', 'jane.smith@example.com', 234567890, 'https://drive.google.com/file/d/1U6pDDv9WFRhMI0eluIkEvHFSqRyQ-3iu/view?usp=drive_link', 1, '2024-06-14', '2024-06-14', 1),
(1, 3, 'user3', 'Michael Johnson', 'michael.johnson@example.com', 989090252, 'https://drive.google.com/file/d/1-Qn8qY38i_0fnahW6u9kI6kJ1nhEm5NA/view?usp=drive_link', 1, '2024-06-15', '2024-06-15', 1),
(1, 4, 'user4', 'Emily Brown', 'emily.brown@example.com', 456789012, 'https://drive.google.com/file/d/1m3pS_sAYXx24P1jUaqM9BSw_wE64eSmD/view?usp=drive_link', 1, '2024-06-16', '2024-06-16', 1),
(1, 5, 'user5', 'David Wilson', 'david.wilson@example.com', 567890124, 'https://drive.google.com/file/d/1KeiVtYxGghm26IMGoPqPS862_m-kyqJA/view?usp=drive_link', 1, '2024-06-17', '2024-06-17', 1);

Insert into Users Values(4, 4, 'user41', 'Tejbir Singh Khalsa', 'tejbir.khalsa@example.com', 45609012, 'https://drive.google.com/file/d/1sTehA4xUcXtp8qitnT6Zwbs-lhZW4XO6/view?usp=drive_link', 1, '2024-06-16','None', '2024-06-16', 1);
select * from Users;
desc users;

CREATE TABLE LOGIN (
    role_id INT(1) NOT NULL,
    uid VARCHAR(50) PRIMARY KEY NOT NULL,
    password VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (role_id) REFERENCES role(role_id),
    FOREIGN KEY (uid) REFERENCES Users(uid)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

select * from Login;
drop table Login;
alter table login modify password VARCHAR(50) NOT NULL;
INSERT INTO LOGIN (role_id, uid, password)
VALUES
(2, 'user2', 'password2'),
(1, 'user1', 'password1'),
(3, 'user3', 'password3'),
(4, 'user4', 'password4'),
(5, 'user5', 'password5');
insert into login values(4,'user41','password41');

CREATE TABLE FLAT_DETAILS (
	uid VARCHAR(50) primary key NOT NULL,
    sid INT(5),
    flat_no varchar(10) not null,
    flat_size varchar(10),
    
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (sid) REFERENCES Society_detail(sid)
);
desc flat_details;
drop table flat_details;
insert into flat_details(uid,sid,flat_no) values('user4',1,'A302'),('user3',1,'A502'),('user2',1,'A902');
select * from flat_details;



CREATE TABLE MyGate_Resident (
    package_id INT(5) AUTO_INCREMENT,
    sid INT(5) NOT NULL,
    flat_no VARCHAR(10) NOT NULL,
    package_desc VARCHAR(255),
    date_arrival DATE NOT NULL,
    time_arrival TIME NOT NULL,
    resident_permission BOOLEAN DEFAULT true NOT NULL,
    
    PRIMARY KEY (package_id),
    FOREIGN KEY (sid) REFERENCES Society_Detail(sid)
);
drop table MyGate_Resident;
desc MyGate_Resident;
CREATE TABLE MyGate_Permission_Security (
	
	package_id INT(5) NOT NULL AUTO_INCREMENT,
    sid INT(5) NOT NULL,
    flat_no varchar(5) NOT NULL,
	package_desc VARCHAR(50),
    date_arrival date NOT NULL,
    time_arrival time NOT NULL,
    permission ENUM('0','1','2') NOT NULL default '0',
    
    Primary key(package_id),
    FOREIGN KEY (sid) REFERENCES Society_Detail(sid)
);
alter table MyGate_Permission_Security modify permission ENUM('0','1','2') NOT NULL default '0'; 
desc MyGate_Permission_Security;
-- alter table MyGate_Permission_Security modify sid INT(5) not null; 
INSERT INTO MyGate_Permission_Security (sid, flat_no, package_desc, time_arrival, date_arrival, permission)
VALUES
(1, 'A302', 'Milk Delivery', '12:00:00', '2024-06-28', '0'),
(1, 'A302', 'Amazon Delivery', '10:30:00', '2024-06-27', '0'),
(1, 'A302', 'Flipkart Delivery', '15:45:00', '2024-06-26', '0');
select * from MyGate_Permission_Security;

CREATE TABLE Notice (
    n_id INT(10) PRIMARY KEY auto_increment,
    sid INT(5) NOT NULL, 
    title VARCHAR(50) NOT NULL,
    content VARCHAR(500) NOT NULL,
    notice_type ENUM('General', 'Urgent', 'Reminder', 'Event') NOT NULL,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (sid) REFERENCES Society_Detail(sid)
);
select * from Notice;
INSERT INTO Notice (sid, title, content, notice_type) VALUES
(1,'Maintenance Notice', 'The building maintenance will be conducted on the 5th of July.', 'General'),
(1,'Urgent Security Update', 'All residents must reset their passwords immediately.', 'Urgent'),
(1,'Meeting Reminder', 'Reminder: Quarterly meeting is scheduled for next Monday.', 'Reminder'),
(1,'Society Picnic', 'Join us for the annual society picnic this Saturday!', 'Event'),
(1,'Office Closure', 'The office will be closed for the holiday on August 15th.', 'General');


CREATE TABLE Documents (
	uid VARCHAR(50) NOT NULL, 
    document_id INT(10) PRIMARY KEY auto_increment,
    doc_name CHAR(20) NOT NULL,
    document_file mediumblob NOT NULL,
    
    foreign key (uid) references Users(uid)
);
select * from Documents;

CREATE TABLE Maintenance_Display (
    mid INT(5) NOT NULL AUTO_INCREMENT,
    sid INT(5) NOT NULL,
    uid VARCHAR(50) NOT NULL,
    bill_amt INT(10) NOT NULL,
    bill_month CHAR(10) NOT NULL,
    bill_year INT(5) NOT NULL,
    payment_status INT(1) NOT NULL DEFAULT 0,
    payment_date DATE,
    PRIMARY KEY (mid),
    FOREIGN KEY (sid) REFERENCES Society_Detail(sid),
    FOREIGN KEY (uid) REFERENCES Users(uid)
);
DROP TRIGGER IF EXISTS set_bill_month_year;

DELIMITER //

CREATE TRIGGER set_bill_month_year
BEFORE INSERT ON Maintenance_Display
FOR EACH ROW
BEGIN
    SET NEW.bill_month = MONTHNAME(CURDATE());
    SET NEW.bill_year = YEAR(CURDATE());
END; //

DELIMITER ;

drop table Maintenance_Display; 
select * from Maintenance_Display;
INSERT INTO Maintenance_Display (sid, uid, bill_amt, payment_status, payment_date)
VALUES
    (1, 'user4', 100, 1, '2024-01-15'),
    (1, 'user4', 200, 0, null),
    (1, 'user4', 75, 1, '2024-03-10');
desc Maintenance_Display;



SELECT *
FROM users AS u
JOIN flat_details AS f ON u.uid = f.uid
JOIN society_detail AS s ON u.sid = s.sid
WHERE u.uid = 'user2';

SELECT * FROM Users as u, Flat_Details as f WHERE u.role_id = 4 AND u.uid = f.uid and u.sid=4;

SELECT * FROM Users as u, Society_Detail as s, Flat_Details as f WHERE u.role_id in (3,4) AND u.sid = s.sid and u.uid = f.uid and u.admin_approval = 1;
SELECT * FROM Users as u, Society_Detail as s, Flat_Details as f WHERE u.role_id in (3,4) AND u.sid = s.sid and u.uid = f.uid order by registration_date desc;

SHOW CREATE TABLE FLAT_DETAILS;
SHOW CREATE TABLE Documents;
SHOW CREATE TABLE Maintenance_Display;
SHOW CREATE TABLE Login;


ALTER TABLE Login  -- Use the actual constraint name here
ADD CONSTRAINT login_ibfk_1
FOREIGN KEY (uid) REFERENCES Users(uid)
ON UPDATE CASCADE
ON delete cascade;


