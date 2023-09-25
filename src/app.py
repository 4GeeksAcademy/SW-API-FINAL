"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Favorites
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_user():

    try:
        all_users = User.query.all()
        user_list = list(map(lambda User: User.serialize(), all_users))

        return jsonify(user_list), 200

    except ValueError as err:

        return {"message": "failed to retrive characters " + err}, 500

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():

    try:
        all_favorites = Favorites.query.all()
        return [ favorites.serialize() for favorites in all_favorites ]

    except ValueError as err:
        return {"message": "failed to retrive The Favorite of the User " + err}, 500
  
    

@app.route('/characters', methods=['GET'])
def get_all_characters():

    try:
        all_characters = Characters.query.all()

        return [character.serialize() for character in all_characters]

    except ValueError as err:
        return {"message": "failed to retrive characters " + err}, 500
    
    
@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):

    try:
        character = Characters.query.get(id)

        if character is None:
            return {"message": "character not found"}, 404

        return character.serialize()

    except ValueError as err:
        return {"message": "failed to retrive character " + err}, 500
    
@app.route("/favorite/character/<int:character_id>", methods=["POST"])
def add_favorite_character(character_id):

    character = Characters.query.get(character_id)
    if not character:
        return {"message": "Character not found"}, 400
    
    favorite_character = Favorites.query.filter_by(character_id=character_id).first()
    if favorite_character:
       return {"message": "Character already in Favorites"}, 400

    # Create a new favorite character
    favorite_character = Favorites(character_id=character_id)
    db.session.add(favorite_character)
    db.session.commit()

    return jsonify({"message": "People added to favorites"})


@app.route('/planets', methods=['GET'])
def get_planets():

    try:
        all_planets = Planets.query.all()
        planets_list = list(
            map(lambda Planets: Planets.serialize(), all_planets))

        return jsonify(planets_list), 200

    except ValueError as err:

        return {"message": "failed to retrive Planets " + err}, 500
    
@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):

    try:
        planet = Planets.query.get(id)

        if planet is None:
            return {"message": "planet not found"}, 404

        return planet.serialize()

    except ValueError as err:
        return {"message": "failed to retrive planet " + err}, 500
    
    
@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):

    planet = Planets.query.get(planet_id)
    if not planet:
        return {"message": "Planet not found"}, 400

    favorite_planet = Favorites.query.filter_by(planet_id=planet_id).first()
    if favorite_planet:
        return {"message": "Planet already a favorite"}, 400

    favorite_planet = Favorites(planet_id=planet_id)
    db.session.add(favorite_planet)
    db.session.commit()

    return jsonify({"message": "Planet added to favorites"})

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return {"message": "Planet Deleted"}, 200

@app.route("/favorite/character/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Characters.query.get(character_id)
    db.session.delete(character)
    db.session.commit()
    return {"message": "Character Deleted"}, 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
