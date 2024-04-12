INSERT INTO members (fname, lname, email, password, current_weight, height) VALUES 
('Alina', 'Shaikhet', 'Alina@example.com', 'password123', 180, 175),
('Robert', 'Collier', 'Robert@example.com', 'password456', 150, 160),
('Ava', 'Emackenie', 'Ava@example.com', 'password789', 200, 180);

INSERT INTO trainers (fname, lname, email, password) VALUES 
('Trainer', 'Alexa', 'trainer1@example.com', 'trainerpassword'),
('Trainer', 'Daryll', 'trainer2@example.com', 'trainerpassword1'),
('Trainer', 'Genkin', 'trainer3@example.com', 'trainerpassword2');

INSERT INTO admins (fname, lname, email, password) VALUES 
('Admin', 'Suzanne', 'admin1@example.com', 'adminpassword'),
('Admin', 'Proshare', 'admin2@example.com', 'adminpassword2');

INSERT INTO trainer_times (trainer_id, availability_date, start_time, end_time) VALUES 
(1, '2024-04-01', '09:00', '11:00'),
(2, '2024-04-01', '13:00', '15:00');

INSERT INTO room_booking (trainer_id, room_number, booking_date, booking_start_time, booking_end_time) VALUES 
(1, 101, '2024-04-01', '09:00', '11:00'),
(2, 102, '2024-04-01', '13:00', '15:00');

INSERT INTO group_classes (class_name, trainer_id, room_number, class_date, class_start_time, class_end_time) VALUES 
('Yoga', 1, 101, '2024-04-02', '10:00', '11:00'),
('Zumba', 2, 102, '2024-04-03', '14:00', '15:00');

INSERT INTO group_class_registrations (group_class_id, member_id) VALUES 
(1, 1),
(2, 2);

INSERT INTO training_sessions (trainer_id, sessions, sessions_start_time, sessions_end_time) VALUES 
(1, '2024-04-02', '09:00', '10:00'),
(2, '2024-04-03', '13:00', '14:00');

INSERT INTO personal_training_registrations (session_id, member_id) VALUES 
(1, 1),
(2, 2);

INSERT INTO equipment_maintenance (equipment_name, maintenance_cost, maintenance_type, status) VALUES 
('bench', 50, 'Repair', 'Fixed'),
('lat pull down machine', 100, 'Repair', 'In Progress' );

INSERT INTO exercises (member_id, exercise_name, reps, sets) VALUES 
(1, 'Push-ups', 15, 3),
(2, 'Squats', 20, 4);

INSERT INTO fitness_achievements (member_id, achievement_name, achievement_desc, achievement_date) VALUES 
(1, 'Ran 5k', 'Completed a 5k run in under 30 minutes', '2024-03-31'),
(2, 'Lost 10 Pounds', 'Achieved weight loss goal of 10 pounds', '2024-03-31');

INSERT INTO fitness_goals (member_id, goal_name, status) VALUES 
(1, 'Run a Marathon', 'In Progress'),
(2, 'Increase Muscle Mass', 'Not Started');

INSERT INTO billing (member_id, payment_amount, payment_date, payment_type) VALUES 
(1, 50.00, '2024-04-01', 'Membership fee'),
(2, 75.00, '2024-04-01', 'personal training fee');
