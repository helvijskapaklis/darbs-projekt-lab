import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'delivery.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Clients(db.Model):
    __tablename__ = 'clients'
    clientID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)      
    surname = db.Column(db.String(100), nullable=False)   
    email = db.Column(db.String(255), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(20), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime, server_default=db.func.now())


class Couriers(db.Model):
    __tablename__ = 'couriers'
    courierID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(20), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime, server_default=db.func.now())


class Routes(db.Model):
    __tablename__ = 'routes'
    routeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clientID = db.Column(db.Integer, db.ForeignKey('clients.clientID'), nullable=False)
    courierID = db.Column(db.Integer, db.ForeignKey('couriers.courierID'), nullable=False)

    locations = db.relationship('Locations', backref='route', lazy=True)


class Locations(db.Model):
    __tablename__ = 'locations'
    locationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    routeID = db.Column(db.Integer, db.ForeignKey('routes.routeID'), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    updatedAt = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

with app.app_context():
    db.create_all()
    if not Clients.query.first():
        c1 = Clients(name="Jānis", surname="Bērziņš", email="janis@example.com", phoneNumber="100001")
        c2 = Clients(name="Līga", surname="Kalniņa", email="liga@example.com", phoneNumber="100002")
        db.session.add_all([c1, c2])
        db.session.commit()

    if not Couriers.query.first():
        co1 = Couriers(name="Mārtiņš", surname="Ozoliņš", email="martins@delivery.com", phoneNumber="200001")
        co2 = Couriers(name="Ilze", surname="Liepiņa", email="ilze@delivery.com", phoneNumber="200002")
        db.session.add_all([co1, co2])
        db.session.commit()

    if not Routes.query.first():
        r1 = Routes(clientID=1, courierID=1)
        r2 = Routes(clientID=2, courierID=2)
        db.session.add_all([r1, r2])
        db.session.commit()

    if not Locations.query.first():
        l1 = Locations(routeID=1, country="Latvija", city="Rīga", address="Brīvības iela 10")
        l2 = Locations(routeID=1, country="Latvija", city="Rīga", address="Dzelzavas iela 20")
        l3 = Locations(routeID=2, country="Latvija", city="Liepāja", address="Rožu iela 3")
        db.session.add_all([l1, l2, l3])
        db.session.commit()
