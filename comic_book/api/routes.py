from flask import Blueprint, request, jsonify
from comic_book.helpers import token_required
from comic_book.models import db, User, Hero, hero_schema, heroes_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getheroes')
@token_required
def get_data(current_user_token):
    return { 'List' : 'Heroes'}


# Create Hero

@api.route('/heroes', methods = ['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    alias = request.json['alias']
    powers = request.json['powers']
    comics_appeared_in = request.json['comics_appeared_in']
    base_of_operations = request.json['base_of_operations']
    user_token = current_user_token.token

    hero = Hero(name, alias, powers, comics_appeared_in, base_of_operations, user_token)
    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)

# Retrieve all Heroes

@api.route('/heroes', methods = ['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token
    heroes = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)


# Retrieve a Hero

@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        hero = Hero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'message' : 'Valid Token Required'}), 401

# Update Hero

@api.route('/heroes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_hero(current_user_token, id):
    hero = Hero.query.get(id) 

    hero.name = request.json['name']
    hero.alias = request.json['alias']
    hero.powers = request.json['powers']
    hero.comics_appeared_in = request.json['comics_appeared_in']
    hero.base_of_operations = request.json['base_of_operations']
    hero.user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)


# Delete Hero

@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)