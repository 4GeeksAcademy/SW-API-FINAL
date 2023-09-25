from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)

    def __init__(self, id, name, rotation_period, orbital_period, gravity, surface_water, diameter):
        self.id = id
        self.name = name
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.gravity = gravity
        self.surface_water = surface_water
        self.diameter = diameter

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
        }


class Characters(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

    name = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    description = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    height = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, hair_color, skin_color, description, gender, eye_color, height, age):
        self.id = id
        self.name = name
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.description = description
        self.gender = gender
        self.eye_color = eye_color
        self.height = height
        self.age = age

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "description": self.description,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "height": self.height,
            "age": self.age,
        }


class Favorites(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship("Planets")

    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship("Characters")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }
