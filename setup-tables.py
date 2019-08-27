import csv
import os

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def create_flights_table():
    """Create flights table if doesn't already exist"""
    try:
        print("Creating 'flights' table..")
        db.execute("CREATE TABLE flights (\
            id SERIAL PRIMARY KEY, \
            origin VARCHAR NOT NULL, \
            destination VARCHAR NOT NULL, \
            duration INTEGER NOT NULL\
            )")
        print("Table 'flights' created")
    except exc.ProgrammingError as err:
        print("Table 'flights' already exists")
    db.commit()


def create_passengers_table():
    """Create passengers table if doesn't already exist"""
    try:
        print("Creating 'passengers' table..")
        db.execute("CREATE TABLE passengers (\
            id SERIAL PRIMARY KEY, \
            name VARCHAR NOT NULL, \
            flight_id INTEGER REFERENCES flights\
            )")
        print("Table 'passengers' created")
    except exc.ProgrammingError as err:
        print("Table 'passengers' already exists")
    db.commit()


def insert_flight_data():
    """Insert data from csv into flights table"""
    # Get data from csv file
    print("Getting data from csv..")
    file = open("flight-info.csv")
    reader = csv.reader(file)

    # Insert csv data into table
    print("Inserting data into 'flights' table..")
    for csv_origin, csv_destination, csv_duration in reader:
        db.execute("INSERT INTO flights (origin, destination, duration)\
            VALUES (:origin, :destination, :duration)", {
            "origin": csv_origin,
            "destination": csv_destination,
            "duration": csv_duration
            })
    print("Data inserted")
    db.commit()


def delete_flights_table():
    """Delete flights table"""
    try:
        print("Attempting to delete table 'flights'")
        db.execute("DROP TABLE flights")
    except exc.ProgrammingError as err:
        print("Table 'flights' does not exist")
    else:
        print("Deleted table 'flights'")

    db.commit()


def delete_passengers_table():
    """Delete passengers table"""
    try:
        print("Attempting to delete table 'passengers'")
        db.execute("DROP TABLE passengers")
    except exc.ProgrammingError as err:
        print("Table 'passengers' does not exist")
    else:
        print("Deleted table 'passengers'")
    db.commit()


def main():
    delete_passengers_table()
    delete_flights_table()
    create_flights_table()
    create_passengers_table()
    insert_flight_data()

if __name__ == "__main__":
    main()
