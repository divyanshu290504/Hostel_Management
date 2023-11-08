drop database if exists hostel_db;
create database hostel_db;
use hostel_db;
create table Hostelite(
	Hostel_ID int primary key auto_increment, 
    Name varchar(20),
    Phone_No varchar(20),
    SRN varchar(20),
    DOB date,
    Legal_ID varchar(20),
    Hostel_Request_Status enum('0','1')
);
create table Local_Guardian(
	Name varchar(20),
    Identification_No varchar(20) primary key,
    DOB date,
    Job varchar(20),
    Phone_No varchar(20),
    Gender enum('Male','Female')
);
create table Room(
	Room_No varchar(20),
    Block_Name varchar(20),
    Floor int,
    No_of_Occupants int,
    Complaint_Type varchar(20),
    Complain_Date date
);
alter table Room add primary key(Room_No,Block_Name);
create table Parent(
	Name varchar(20),
    Relation varchar(20),
    DOB date,
    Job varchar(20),
    Phone_No varchar(20),
    Identification_No varchar(20)
);
alter table Parent add primary key(Identification_No);
create table Mess(
	Mess_Name varchar(20),
    Month varchar(20),
    Year int,
    Hostel_ID int primary key,
    foreign key(Hostel_ID) references Hostelite(Hostel_ID)
);
create table Leave_Request(
	Verification_Status varchar(20),
    Reason varchar(100),
    Place varchar(20),
    Arrival_Datetime timestamp,
    Leaving_Datetime timestamp,
    Hostel_ID int primary key,
    foreign key(Hostel_ID) references Hostelite(Hostel_ID)
);
create table Has_LG(
	Hostel_ID int,
    Identification_No varchar(20),
    Relation varchar(20)
);
alter table Has_LG add primary key(Hostel_ID,Identification_No);
alter table Has_LG
add foreign key(Hostel_ID) references Hostelite(Hostel_ID);
create table Hostelite_Addr(
	Hostelite_ID int,
    House_Details varchar(20),
    State varchar(20),
    City varchar(20),
    Pincode int,
    foreign key(Hostelite_ID) references Hostelite(Hostel_ID)
);
create table Local_Guardian_Addr(
	LG_ID varchar(20),
    House_Details varchar(20),
    State varchar(20),
    City varchar(20),
    Pincode int,
    foreign key(LG_ID) references Local_Guardian(Identification_No)
);
create table HasParent_Guardian(
	Hostelite_ID int,
    ID_Parent varchar(20),
    Relation varchar(20)
);

create table if not exists `accounts`(
	`id` int(11) not null auto_increment,
	`username` varchar(50) not null,
	`password` varchar(255) not null,
    `email` varchar(100) not null,
    primary key(`id`)
) engine=InnoDB auto_increment=1 default charset=utf8mb4;

alter table HasParent_Guardian add primary key(Hostelite_ID,ID_Parent);
alter table HasParent_Guardian 
add foreign key(Hostelite_ID) references Hostelite(Hostel_ID);
alter table HasParent_Guardian 
add foreign key(ID_Parent) references Parent(Identification_No);

insert into accounts values(NULL,'h1','h1','h1@gmail.com');
insert into accounts values(NULL,'a1','a1','a1@gmail.com');

-- Extra Queries Added Here
alter table mess drop constraint mess_ibfk_1;
alter table mess add constraint fk1 foreign key(Hostel_ID) REFERENCES hostelite(Hostel_ID) on delete cascade;

alter table leave_request drop constraint leave_request_ibfk_1;
alter table leave_request add constraint leave_request_ibfk_1 foreign key(Hostel_ID) references Hostelite(Hostel_ID) on delete cascade;

alter table has_lg drop constraint has_lg_ibfk_1;
alter table has_lg add constraint has_lg_ibfk_1 foreign key(Hostel_ID) references Hostelite(Hostel_ID) on delete cascade;

alter table hostelite_addr drop constraint hostelite_addr_ibfk_1;
alter table hostelite_addr add constraint hostelite_addr_ibfk_1 foreign key(Hostelite_ID) references Hostelite(Hostel_ID) on delete cascade;

alter table local_guardian_addr drop constraint local_guardian_addr_ibfk_1;
alter table local_guardian_addr add constraint local_guardian_addr_ibfk_1 foreign key(LG_ID) references Local_Guardian(Identification_No) on delete cascade;

alter table hasparent_guardian drop constraint hasparent_guardian_ibfk_1;
alter table hasparent_guardian add constraint hasparent_guardian_ibfk_1 foreign key(Hostelite_ID) references Hostelite(Hostel_ID) on delete cascade;

alter table hasparent_guardian drop constraint hasparent_guardian_ibfk_2;

alter table Has_LG drop constraint has_lg_ibfk_2;

alter table Local_Guardian add foreign key(Identification_No) references has_lg(Identification_No) on delete cascade;

alter table parent add foreign key(Identification_No) references hasParent_Guardian(ID_Parent) on delete cascade;


-- Hostelite 1
INSERT INTO hostelite VALUES (NULL, 'John Doe', '1234567890', 'PES1UG21CS001', '2000-01-01', '123456789012', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '123 Main St', 'Sample State', 'Sample City', '123456');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019178', 'Mother');
INSERT INTO Parent VALUES ('Jane Doe', 'Mother', '1980-01-01', 'Sample Job', '1234567890', '8523019178');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679167', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Alice Smith', '916791679167', '1985-01-01', 'Sample Job', '9876543210', 'Female');
INSERT INTO Local_Guardian_Addr VALUES ('916791679167', '456 Elm St', 'LG State', 'LG City', '654321');

-- Hostelite 2
INSERT INTO hostelite VALUES (NULL, 'Michael Johnson', '9876543210', 'PES1UG21CS002', '2000-02-02', '987654321098', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '456 Elm St', 'Sample State', 'Sample City', '654321');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019179', 'Father');
INSERT INTO Parent VALUES ('David Johnson', 'Father', '1975-02-02', 'Sample Job', '9876543210', '8523019179');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679166', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Sara Smith', '916791679166', '1980-01-01', 'Sample Job', '9876543211', 'Female');
INSERT INTO Local_Guardian_Addr VALUES ('916791679166', '789 Oak St', 'LG State', 'LG City', '753159');

-- Hostelite 3
INSERT INTO hostelite VALUES (NULL, 'Robert Williams', '8765432109', 'PES1UG21CS003', '1999-03-03', '876543210987', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '789 Oak St', 'Sample State', 'Sample City', '753159');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019278', 'Mother');
INSERT INTO Parent VALUES ('Jessica Williams', 'Mother', '1981-03-03', 'Sample Job', '8765432109', '8523019278');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679165', 'Guardian');
INSERT INTO Local_Guardian VALUES ('William Smith', '916791679165', '1982-03-03', 'Sample Job', '9876543212', 'Male');
INSERT INTO Local_Guardian_Addr VALUES ('916791679165', '123 Pine St', 'LG State', 'LG City', '852654');

-- Hostelite 4
INSERT INTO hostelite VALUES (NULL, 'Sarah Anderson', '7654321098', 'PES1UG21CS004', '1999-04-04', '765432109876', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '123 Pine St', 'Sample State', 'Sample City', '852654');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019378', 'Father');
INSERT INTO Parent VALUES ('Michael Anderson', 'Father', '1982-04-04', 'Sample Job', '7654321098', '8523019378');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679164', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Emily Smith', '916791679164', '1983-04-04', 'Sample Job', '9876543213', 'Female');
INSERT INTO Local_Guardian_Addr VALUES ('916791679164', '456 Maple St', 'LG State', 'LG City', '958743');

-- Hostelite 5
INSERT INTO hostelite VALUES (NULL, 'James Wilson', '6543210987', 'PES1UG21CS005', '1998-05-05', '654321098765', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '456 Maple St', 'Sample State', 'Sample City', '958743');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019478', 'Mother');
INSERT INTO Parent VALUES ('Maria Wilson', 'Mother', '1978-05-05', 'Sample Job', '6543210987', '8523019478');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679163', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Daniel Smith', '916791679163', '1985-05-05', 'Sample Job', '9876543214', 'Male');
INSERT INTO Local_Guardian_Addr VALUES ('916791679163', '789 Cedar St', 'LG State', 'LG City', '852964');

-- Hostelite 6
INSERT INTO hostelite VALUES (NULL, 'Mary Brown', '5432109876', 'PES1UG21CS006', '1998-06-06', '543210987654', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '789 Cedar St', 'Sample State', 'Sample City', '852964');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019578', 'Father');
INSERT INTO Parent VALUES ('John Brown', 'Father', '1979-06-06', 'Sample Job', '5432109876', '8523019578');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679162', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Olivia Smith', '916791679162', '1986-06-06', 'Sample Job', '9876543215', 'Female');
INSERT INTO Local_Guardian_Addr VALUES ('916791679162', '123 Walnut St', 'LG State', 'LG City', '975432');

-- Hostelite 7
INSERT INTO hostelite VALUES (NULL, 'William Davis', '4321098765', 'PES1UG21CS007', '1997-07-07', '432109876543', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '123 Walnut St', 'Sample State', 'Sample City', '975432');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019678', 'Mother');
INSERT INTO Parent VALUES ('Sophia Davis', 'Mother', '1980-07-07', 'Sample Job', '4321098765', '8523019678');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679161', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Alexander Smith', '916791679161', '1987-07-07', 'Sample Job', '9876543216', 'Male');
INSERT INTO Local_Guardian_Addr VALUES ('916791679161', '456 Birch St', 'LG State', 'LG City', '753951');

-- Hostelite 8
INSERT INTO hostelite VALUES (NULL, 'Jennifer Martinez', '3210987654', 'PES1UG21CS008', '1997-08-08', '321098765432', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '456 Birch St', 'Sample State', 'Sample City', '753951');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019778', 'Father');
INSERT INTO Parent VALUES ('David Martinez', 'Father', '1978-08-08', 'Sample Job', '3210987654', '8523019778');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679160', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Mia Smith', '916791679160', '1988-08-08', 'Sample Job', '9876543217', 'Female');
INSERT INTO Local_Guardian_Addr VALUES ('916791679160', '789 Spruce St', 'LG State', 'LG City', '854732');

-- Hostelite 9
INSERT INTO hostelite VALUES (NULL, 'David Taylor', '2109876543', 'PES1UG21CS009', '1996-09-09', '210987654321', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '789 Spruce St', 'Sample State', 'Sample City', '854732');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019878', 'Mother');
INSERT INTO Parent VALUES ('Olivia Taylor', 'Mother', '1979-09-09', 'Sample Job', '2109876543', '8523019878');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679159', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Lucas Smith', '916791679159', '1989-09-09', 'Sample Job', '9876543218', 'Male');
INSERT INTO Local_Guardian_Addr VALUES ('916791679159', '123 Cedar St', 'LG State', 'LG City', '753214');

-- Hostelite 10
INSERT INTO hostelite VALUES (NULL, 'Linda White', '1098765432', 'PES1UG21CS010', '1996-10-10', '109876543210', '0');
INSERT INTO hostelite_addr VALUES (LAST_INSERT_ID(), '123 Cedar St', 'Sample State', 'Sample City', '753214');
INSERT INTO HasParent_Guardian VALUES (LAST_INSERT_ID(), '8523019978', 'Father');
INSERT INTO Parent VALUES ('Daniel White', 'Father', '1977-10-10', 'Sample Job', '1098765432', '8523019978');
INSERT INTO Has_LG VALUES (LAST_INSERT_ID(), '916791679158', 'Guardian');
INSERT INTO Local_Guardian VALUES ('Sophia Smith', '916791679158', '1990-10-10', 'Sample Job', '9876543219', 'Female');
INSERT INTO Local_Guardian_Addr VALUES ('916791679158', '456 Fir St', 'LG State', 'LG City', '852964');
