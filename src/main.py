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
from models import db, User, Favorite_planet, Favorite_character, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

#USUARIOS

@app.route('/user', methods=['GET'])
def get_user():
    user = User.query.filter().all()
    result = list(map(lambda user: user.serialize(), user))
    response_body = {
    "usuarios": result,
    "msg": "Usuarios"
    }

    return jsonify(response_body), 200

#Planetas y planetas singulares

@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.filter().all()
    result = list(map(lambda planet: planet.serialize(), planets))
    response_body = {
    "usuarios": result,
    "msg": "Planet"
    }

    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_singleplanet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200

#Personajes y personajes singulares

@app.route('/character', methods=['GET'])
def get_character():
    characters = Character.query.filter().all()
    result = list(map(lambda character: character.serialize(), character))
    response_body = {
    "usuarios": result,
    "msg": "Character"
    }

    return jsonify(response_body), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_singlecharacter(character_id):
    Character = Character.query.get(character_id)
    return jsonify(character.serialize()), 200

#Favoritos Character y Planet

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    # users = User.query.filter().all()
    # User.query.filter_by(username=username).all()
    characters = Favorite_character.query.filter_by(user_id=user_id).all()
    planet = Favorite_planet.query.filter_by(user_id=user_id).all()
    result = (list(map(lambda character: character.serialize(), characters)),
        list(map(lambda planet: planet.serialize(), planet)))
    return jsonify(result), 200

@app.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods=['POST'])
def add_favorites_characters(user_id, character_id):
    added_characters = Favorite_character(user_id = int(user_id), character_id = int(character_id))
    db.session.add(added_characters)
    db.session.commit()
    result = {"msg": "Favorito agregado"}
    return jsonify(result), 200

@app.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    deleted_character = Favorite_character.query.filter_by(character_id=character_id, user_id=user_id).first()
    db.session.delete(deleted_character)
    db.session.commit()
    result = {"msg": "Favorito eliminado"}
    return jsonify(result), 200

@app.route('/user/<int:user_id>/favorites/planets/<int:planets_id>', methods=['POST'])
def add_favorites_planet(user_id, planets_id):
    added_planet = Favorite_planet(user_id = int(user_id), planets_id = int(planets_id))
    db.session.add(added_planet)
    db.session.commit()
    result = {"msg": "Favorito agregado"}
    return jsonify(result), 200

@app.route('/user/<int:user_id>/favorites/planets/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planets_id):
    deleted_planet = Favorite_planet.query.filter_by(planets_id=planets_id, user_id=user_id).first()
    db.session.delete(deleted_planet)
    db.session.commit()
    result = {"msg": "Favorito eliminado"}
    return jsonify(result), 200


       

# this only runs if `$ python src/main.py` is executed
    if __name__ == '__main__':
        PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
