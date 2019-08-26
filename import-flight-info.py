import csv
import os

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    """Create table and insert data from csv file."""
    # Create flights table if doesn't already exist
    try:
        print("Creating table..")
        db.execute("CREATE TABLE flights (\
            id SERIAL PRIMARY KEY, \
            origin VARCHAR NOT NULL, \
            destination VARCHAR NOT NULL, \
            duration INTEGER NOT NULL\
            )")
        print("Table created")
    except exc.ProgrammingError as err:
        print("Table already exists")

    # Get data from csv file
    print("Getting data from csv..")
    file = open("flight-info.csv")
    reader = csv.reader(file)

    # Insert csv data into table
    print("Inserting data into table..")
    for csv_origin, csv_destination, csv_duration in reader:
        db.execute("INSERT INTO flights (origin, destination, duration)\
            VALUES (:origin, :destination, :duration)", {
            "origin": csv_origin,
            "destination": csv_destination,
            "duration": csv_duration
            })
    print("Data inserted")

    db.commit()

if __name__ == "__main__":
    main()
