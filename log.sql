-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28
AND street = "Humphrey Street";

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who
-- were present at the time – each of their interview transcripts mentions the bakery.

-- We can find more information by studying the interviews
SELECT transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28
AND transcript LIKE "%bakery%";

-- 1: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have
-- security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

-- 2: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
-- I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

-- 3: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they
-- were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Use the first interview's information :
SELECT people.name FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE year = 2021 AND day = 28 AND month = 7
AND hour = 10 AND minute >= 15 AND minute <= 25
AND activity = 'exit';

-- Suspects : Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey

-- Use the second interview's information
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2021 AND day = 28 AND month = 7
AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street';

-- Suspects : Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista
-- Common suspects : Bruce, Diana, Iman, Luca

-- Use the third interview's information
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2021 AND day = 28 AND month = 7
AND duration < 60;

-- Suspects : Sofia, Kelsey, Bruce, Taylor, Diana, Carina, Kenny, Benista
-- Common Suspects : Diana, Bruce

-- Use more information from the third interview:
SELECT hour, minute, name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE year = 2021 AND day = 29 AND month = 7
AND full_name LIKE "%Fiftyville%" AND city = "Fiftyville"
ORDER BY hour;

-- The earliest flight at 8:20 was taken by Bruce not Diana, hence, Bruce is the thief of the CS50 Duck

-- The city the thief escaped to:
SELECT city FROM airports
JOIN flights ON flights.destination_airport_id = airports.id
WHERE year = 2021 AND day = 29 AND month = 7
AND hour = 8 AND minute = 20
AND origin_airport_id = (SELECT id FROM airports WHERE full_name LIKE "%Fiftyville%");

-- City : New York City

-- Getting the phone number of Bruce for the future
SELECT phone_number FROM people WHERE name = 'Bruce';
-- phone number = (367) 555-5533

-- The accomplice of Bruce is :
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
AND caller = '(367) 555-5533'
AND year = 2021 AND month = 7 AND day = 28
AND duration < 60;

-- Suspects : Robin
-- Hence, Robin is Bruce's accomplice