import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    """Show form to book a flight"""
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight with passenger's name"""
    # Get passenger's name
    passenger_name = request.form.get("passenger_name")

    # Get flight selected by passenger
    flight_id = request.form.get("flight_id")

    flight = db.execute("SELECT origin, destination FROM flights \
        WHERE id = :flight_id", {"flight_id": flight_id}).fetchone()

    db.execute("INSERT INTO passengers (name, flight_id) \
        VALUES (:name, :flight_id)",
        {"name": passenger_name, "flight_id": flight_id})
    db.commit()

    return render_template("success.html", flight=flight, passenger=passenger_name)

@app.route("/manage")
def manage():
    """Display all available flights"""
    flights = db.execute("SELECT id, origin, destination FROM flights").fetchall()
    db.commit()
    return render_template("manage.html", flights=flights)

@app.route("/manage/<int:flight_id>")
def flight(flight_id):
    """Show info about a flight"""
    flight = db.execute("SELECT origin, destination, duration FROM flights \
        WHERE id=:flight_id", {"flight_id": flight_id}).fetchone()
    passengers = db.execute("SELECT name FROM passengers \
        WHERE flight_id=:flight_id", {"flight_id": flight_id}).fetchall()
    return render_template("flight.html", flight=flight, passengers=passengers)
