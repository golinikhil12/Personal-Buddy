from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    time = db.Column(db.String(50))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    done = db.Column(db.Boolean, default=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50))
    journal = db.Column(db.Text)
    timestamp = db.Column(db.String(50))

class HealthLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    water_intake = db.Column(db.String(50))
    sleep_hours = db.Column(db.String(50))
    steps = db.Column(db.String(50))
