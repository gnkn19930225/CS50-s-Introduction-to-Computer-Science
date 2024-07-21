-- Keep a log of any SQL queries you execute as you solve the mystery.
-- First of all, the known information is that on July 28, 2023, a theft occurred on Humphrey Street in the town of Fiftyville.
-- I must use fiftyville.db to investigate who is the thief? Who are the accomplices? Which city did the thief finally escape to?
-- Before using fiftyville.db to investigate who is the thief, you must first check what tables fiftyville.db contains. So the first step is .schema
.schema
-- The “fiftyville.db” contains the following tables :crime_scene_reports、interviews、atm_transactions、bank_accounts、airports、flights、passengers、phone_calls、people、bakery_security_logs
-- Among them, crime_scene_reports includes street, year, month, and day. I can search through known information.
SELECT
    *
FROM
    crime_scene_reports
WHERE
    street = 'Humphrey Street'
    AND YEAR = 2023
    AND MONTH = 7
    AND DAY = 28;

-- Two cases occurred that day, among which ID 295 is the case to be investigated this time, so I added the search conditions to the results of 'contains CS50 duck'
SELECT
    description
FROM
    crime_scene_reports
WHERE
    street = 'Humphrey Street'
    AND YEAR = 2023
    AND MONTH = 7
    AND DAY = 28
    AND description LIKE '%CS50 duck%';

--The results investigated by crime_scene_reports indicate that three witnesses mentioned this bakery
--so I used bakery as the keyword to search interviews to see what results there were.
SELECT
    transcript
FROM
    interviews
WHERE
    YEAR >= 2023
    AND MONTH >= 7
    AND DAY >= 28
    AND transcript LIKE '%bakery%';

--A lot of useful information was found in the statements of three witnesses:
--1. You can find the car leaving the parking lot from the bakery’s security video. Maybe there will be clues.
--2. The thief withdrew money from the cash machine that morning
--3. The thief called his accomplice and asked him to take the earliest flight out of Fiftyville the next day and asked his accomplice to buy a ticket.
--I continue to look for clues based on what the witnesses said.
SELECT
    *
FROM
    bakery_security_logs
WHERE
    YEAR = 2023
    AND MONTH = 7
    AND DAY = 28
    AND HOUR = 10
    AND MINUTE >= 15
    AND MINUTE <= 25
    AND activity = 'exit';

SELECT
    *
FROM
    people
WHERE
    id IN (
        SELECT
            person_id
        FROM
            bank_accounts
            JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
        WHERE
            atm_transactions.YEAR = 2023
            AND atm_transactions.MONTH = 7
            AND atm_transactions.DAY = 28
            AND atm_transactions.atm_location = 'Leggett Street'
            AND atm_transactions.transaction_type = 'withdraw'
    );

SELECT
    *
FROM
    phone_calls
WHERE
    YEAR = 2023
    AND MONTH = 7
    AND DAY = 28
    AND duration < 60;

SELECT
    *
FROM
    passengers
WHERE
    flight_id IN (
        SELECT
            id
        FROM
            flights
        WHERE
            YEAR = 2023
            AND MONTH = 7
            AND DAY = 29
        ORDER BY
            HOUR ASC,
            MINUTE ASC
        LIMIT
            1
    );

SELECT
    full_name,
    city
FROM
    airports
WHERE
    id IN (
        SELECT
            destination_airport_id
        FROM
            flights
        WHERE
            YEAR = 2023
            AND MONTH = 7
            AND DAY = 29
        ORDER BY
            HOUR ASC,
            MINUTE ASC
        LIMIT
            1
    );

--Now I have found some relevant information through the witnesses' statements
--(the possible license plate of the thief, the person who may be the thief and related information,
--the conversation record between the thief and his accomplices,
--the passengers on the plane on which the thief escaped)
--next Cross-referencing this information can identify the thief and his accomplices.
--The only thing that is certain at present is that the thief will escape to New York City.
SELECT
    name
FROM
    people
WHERE
    license_plate IN (
        SELECT
            license_plate
        FROM
            bakery_security_logs
        WHERE
            YEAR = 2023
            AND MONTH = 7
            AND DAY = 28
            AND HOUR = 10
            AND MINUTE >= 15
            AND MINUTE <= 25
            AND activity = 'exit'
    )
    AND id IN (
        SELECT
            id
        FROM
            people
        WHERE
            id IN (
                SELECT
                    person_id
                FROM
                    bank_accounts
                    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
                WHERE
                    atm_transactions.YEAR = 2023
                    AND atm_transactions.MONTH = 7
                    AND atm_transactions.DAY = 28
                    AND atm_transactions.atm_location = 'Leggett Street'
                    AND atm_transactions.transaction_type = 'withdraw'
            )
    )
    AND phone_number IN (
        SELECT
            caller
        FROM
            phone_calls
        WHERE
            YEAR = 2023
            AND MONTH = 7
            AND DAY = 28
            AND duration < 60
    )
    AND passport_number IN (
        SELECT
            passport_number
        FROM
            passengers
        WHERE
            flight_id IN (
                SELECT
                    id
                FROM
                    flights
                WHERE
                    YEAR = 2023
                    AND MONTH = 7
                    AND DAY = 29
                ORDER BY
                    HOUR ASC,
                    MINUTE ASC
                LIMIT
                    1
            )
    );

--The thief is Bruce
SELECT
    name
FROM
    people
WHERE
    phone_number IN (
        SELECT
            receiver
        FROM
            phone_calls
        WHERE
            YEAR = 2023
            AND MONTH = 7
            AND DAY = 28
            AND duration < 60
            AND caller IN (
                SELECT
                    phone_number
                FROM
                    people
                WHERE
                    license_plate IN (
                        SELECT
                            license_plate
                        FROM
                            bakery_security_logs
                        WHERE
                            YEAR = 2023
                            AND MONTH = 7
                            AND DAY = 28
                            AND HOUR = 10
                            AND MINUTE >= 15
                            AND MINUTE <= 25
                            AND activity = 'exit'
                    )
                    AND id IN (
                        SELECT
                            id
                        FROM
                            people
                        WHERE
                            id IN (
                                SELECT
                                    person_id
                                FROM
                                    bank_accounts
                                    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
                                WHERE
                                    atm_transactions.YEAR = 2023
                                    AND atm_transactions.MONTH = 7
                                    AND atm_transactions.DAY = 28
                                    AND atm_transactions.atm_location = 'Leggett Street'
                                    AND atm_transactions.transaction_type = 'withdraw'
                            )
                    )
                    AND phone_number IN (
                        SELECT
                            caller
                        FROM
                            phone_calls
                        WHERE
                            YEAR = 2023
                            AND MONTH = 7
                            AND DAY = 28
                            AND duration < 60
                    )
                    AND passport_number IN (
                        SELECT
                            passport_number
                        FROM
                            passengers
                        WHERE
                            flight_id IN (
                                SELECT
                                    id
                                FROM
                                    flights
                                WHERE
                                    YEAR = 2023
                                    AND MONTH = 7
                                    AND DAY = 29
                                ORDER BY
                                    HOUR ASC,
                                    MINUTE ASC
                                LIMIT
                                    1
                            )
                    )
            )
    );

--The thief's accomplice is Robin
SELECT
    city
FROM
    airports
WHERE
    id IN (
        SELECT
            destination_airport_id
        FROM
            flights
        WHERE
            YEAR = 2023
            AND MONTH = 7
            AND DAY = 29
        ORDER BY
            HOUR ASC,
            MINUTE ASC
        LIMIT
            1
    );
