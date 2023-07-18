from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'Car Collector: {current_user_token.token}')

    contact = Contact(first_name, last_name, email, phone_number, address, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contacts(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)


@api.route('/contacts/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)


@api.route('/contacts/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    contact = Contact.query.get(id) 
    contact.email = request.json['email']
    contact.first_name = request.json['first_name']
    contact.last_name = request.json['last_name']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)


@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    vin = request.json['vin']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_id = current_user_token.token 
    
    
    car = Car(vin, make, model, year, color, user_id = user_id)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)



@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    user_id = current_user_token.token 
    cars = Car.query.filter_by(user_id = user_id).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car_Token = current_user_token.token
    if car_Token == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': "Invalid Token"}), 401


@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id) 
    car.vin = request.json['vin']
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.user_id = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)