import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight with passenger's name"""
    # Get passenger's name
    passenger_name = request.form.get("passenger_name")

    # Get flight selected by passenger
    flight_id = request.form.get("flight_id")

    flight_info = db.execute("SELECT origin, destination FROM flights \
        WHERE id = :flight_id", {"flight_id": flight_id}).fetchone()

    db.execute("INSERT INTO passengers (name, flight_id) \
        VALUES (:name, :flight_id)",
        {"name": passenger_name, "flight_id": flight_id})
    db.commit()

    return render_template("success.html", origin=flight_info[0],
        destination=flight_info[1], passenger=passenger_name)
