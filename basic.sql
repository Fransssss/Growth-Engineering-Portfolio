DROP TABLE IF EXISTS user_events;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admin;

CREATE TABLE user_events (
	user_id INTEGER NOT NULL,
	event_name TEXT NOT NULL,
	created_at DATETIME NOT NULL,
	country TEXT NOT NULL
);

CREATE TABLE users (
	user_id INTEGER NOT NULL,
	name TEXT NOT NULL,
	plan TEXT NOT NULL,
	signup_date DATE NOT NULL
);

CREATE TABLE admin (
	the_rank INTEGER NOT NULL,
	name TEXT NOT NULL,
	role TEXT NOT NULL
);

BEGIN TRANSACTION;

INSERT INTO users (user_id, name, plan, signup_date) VALUES
	(1, 'Alice', 'pro',  '2024-01-01'),
	(2, 'Bob',   'free', '2024-01-01'),
	(3, 'Carol', 'pro',  '2024-01-02'),
	(4, 'Dan',   'free', '2024-01-03'),
	(7, 'Eve',   'free', '2024-01-07'),
	(8, 'Frank', 'free', '2024-01-07'),
	(9, 'Grace', 'free', '2024-01-08'),
	(10, 'Hank', 'free', '2024-01-08');

INSERT INTO user_events (user_id, event_name, created_at, country) VALUES
	(1, 'signed_up',       '2024-01-01 09:00:00', 'US'),
	(1, 'sent_message',    '2024-01-01 09:05:00', 'US'),
	(2, 'signed_up',       '2024-01-01 10:00:00', 'UK'),
	(2, 'sent_message',    '2024-01-01 10:12:00', 'UK'),
	(3, 'signed_up',       '2024-01-02 08:00:00', 'US'),
	(3, 'sent_message',    '2024-01-02 08:10:00', 'US'),
	(3, 'upgraded_to_pro', '2024-01-02 08:30:00', 'US'),
	(4, 'signed_up',       '2024-01-03 14:20:00', 'CA'),
	(4, 'sent_message',    '2024-01-03 14:45:00', 'CA'),
	(5, 'signed_up',       '2024-01-04 11:05:00', 'UK'),
	(5, 'upgraded_to_pro', '2024-01-05 09:00:00', 'UK'),
	(6, 'signed_up',       '2024-01-06 16:30:00', 'US'),
	(7, 'signed_up',       '2024-01-07 10:00:00', 'US'),
	(8, 'signed_up',       '2024-01-07 11:00:00', 'US'),
	(8, 'sent_message',    '2024-01-07 11:05:00', 'US'),
	(9, 'signed_up',       '2024-01-08 09:00:00', 'CA'),
	(9, 'sent_message',    '2024-01-08 09:10:00', 'CA'),
	(9, 'upgraded_to_pro', '2024-01-08 09:30:00', 'CA'),
	(10, 'signed_up',      '2024-01-08 14:00:00', 'US'),
	(10, 'sent_message',   '2024-01-08 14:10:00', 'US');

INSERT INTO admin (the_rank, name, role) VALUES
(1, 'Frans', 'Growth CEO');

COMMIT;