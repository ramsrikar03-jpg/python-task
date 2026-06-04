-- Run this script in MySQL Workbench before starting the Flask app.
-- Default connection: localhost:3306, user root (adjust as needed).

CREATE DATABASE IF NOT EXISTS movie_ticket_booking
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE movie_ticket_booking;

-- Tables are created automatically by Flask (db.create_all()) on first run.
-- After starting the app, refresh the Schemas panel in Workbench to see:
-- users, movie, shows, booking, ticket
