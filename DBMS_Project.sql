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
