create table members(
    member_id serial primary key,
    fname varchar(26) not null,
    lname varchar(26) not null,
    email varchar(26) not null unique,
    password varchar(26) not null,
    current_weight integer not null,
    height integer not null
);

create table trainers(
    trainer_id serial primary key,
    fname varchar(26) not null,
    lname varchar(26) not null,
    email varchar(26) not null unique,
    password varchar(26) not null
);

create table admins(
    admin_id serial primary key,
    fname varchar(26) not null,
    lname varchar(26) not null,
    email varchar(26) not null unique,
    password varchar(26) not null
);

create table trainer_times(
    time_id serial primary key,
    trainer_id integer references trainers(trainer_id),
    availability_date DATE,
    start_time TIME,
    end_time TIME
);

create table room_booking(
    booking_id serial primary key,
    trainer_id integer references trainers(trainer_id),
    room_number integer not null,
    booking_date DATE,
    booking_start_time TIME,
    booking_end_time TIME,
	unique(room_number)
);

create table group_classes(
    group_classes_id serial primary key,
    class_name varchar(26) not null,
    trainer_id integer references trainers(trainer_id),
    room_number integer references room_booking(room_number),
    class_date DATE,
    class_start_time TIME,
    class_end_time TIME
);

CREATE TABLE group_class_registrations (
    registration_id SERIAL PRIMARY KEY,
    group_class_id INT REFERENCES group_classes(group_classes_id),
    member_id INT REFERENCES members(member_id)
);

create table training_sessions(
    session_id serial primary key,
    trainer_id integer references trainers(trainer_id),
    sessions DATE,
    sessions_start_time TIME,
    sessions_end_time TIME
);

CREATE TABLE personal_training_registrations (
    registration_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES training_sessions(session_id),
    member_id INT REFERENCES members(member_id)
);


CREATE TYPE equipment_status AS ENUM ('Not fixed', 'In Progress', 'Fixed');
create table equipment_maintenance(
    maintenance_id serial primary key,
    equipment_name varchar(50) not null,
    maintenance_cost integer not null,
    maintenance_type varchar(50) not null,
    status equipment_status
);

create table exercises(
    exercise_id serial primary key,
    member_id integer references members(member_id),
    exercise_name varchar(26) not null,
    reps integer not null,
    sets integer not null
);

CREATE TABLE fitness_achievements (
    achievement_id serial primary key,
    member_id integer references members(member_id),
    achievement_name varchar(100) not null,
    achievement_desc text not null,
    achievement_date date not null
);

CREATE TYPE goal_status AS ENUM ('Not Started', 'In Progress', 'Completed');

CREATE TABLE fitness_goals (
    goal_id serial primary key,
    member_id integer references members(member_id),
    goal_name varchar(100) not null,
    status goal_status
);

create table billing(
    billing_id serial primary key,
    member_id integer references members(member_id),
    payment_amount decimal not null,
    payment_date date not null,
    payment_type varchar(100) not null
);
