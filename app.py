from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cd_collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    country = db.Column(db.String(4))
    phone = db.Column(db.String(100), nullable=False, unique=True)
    isPublic = db.Column(db.Boolean)
    image = db.Column(db.String(100))


# создаем базу данных, если ее пока нет
with app.app_context():
    db.create_all()


def present_person(user):
    return {
        'id': user.id,
        'email': user.email,
        'login': user.login,
        'name': user.name,
        'description': user.description,
        'country': user.country,
        'phone': user.phone,
        'isPublic': user.isPublic,
        'image': user.image
    }


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    alpha2 = db.Column(db.String(3), nullable=False)
    alpha3 = db.Column(db.String(4), nullable=False)
    region = db.Column(db.String(100))


# создаем базу данных, если ее пока нет
with app.app_context():
    db.create_all()


def present_country(country):
    return {
        'id': country.id,
        'name': country.name,
        'alpha2': country.alpha2,
        'alpha3': country.alpha3,
        'region': country.region
    }


@app.route('/api/countries', methods=['GET'])
def get_all_countries():
    # забираем всех исполнителей из базы
    countries = Country.query.all()
    # превращаем их в список словарей
    countries_descriptions = [present_country(country) for country in countries]
    # возвращаем ответ в виде списка словарей и типом application/json
    return jsonify(countries_descriptions)


@app.route('/api/country/<string:alpha>', methods=['GET'])
def get_artist_by_id(alpha):
    alpha2 = Country.query.filter_by(alpha2=alpha).first()
    if not alpha2:
        return jsonify({'reason': 'Alpha2 not found'}), 404
    return jsonify(present_country(alpha2)), 200


@app.route('/api/registration', methods=['POST'])
def add_person():
    # получаем данные, отправленные пользователем в формате словаря
    data = request.get_json()
    if data is None:
        return jsonify({'reason': 'Invalid JSON format'}), 400
    login = data.get('login')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    description = data.get('description')
    country = data.get('country')
    phone = data.get('phone')
    isPublic = data.get('isPublic')
    image = data.get('image')

    if not login:
        return jsonify({'reason': 'Missing login'}), 400

    if not email:
        return jsonify({'reason': 'Missing email'}), 400

    if not phone:
        return jsonify({'reason': 'Missing phone'}), 400

    if not password:
        return jsonify({'reason': 'Missing password'}), 400

    if isPublic != True and isPublic != False:
        return jsonify({'reason': 'Missing isPublic'}), 400

    if Person.query.filter_by(name=name).first():
        return jsonify({'reason': 'Person already exists'}), 400
    if Person.query.filter_by(login=login).first():
        return jsonify({'reason': 'Person already exists'}), 400
    if Person.query.filter_by(email=email).first():
        return jsonify({'reason': 'Person already exists'}), 400
    if Person.query.filter_by(phone=phone).first():
        return jsonify({'reason': 'Person already exists'}), 400
    print(login, name)
    user = Person(login=login, name=name, email=email, password=password, description=description, country=country,
                  phone=phone, isPublic=isPublic, image=image)

    db.session.add(user)
    db.session.commit()
    return jsonify(present_person(user))

@app.route('/api/delete/<string:name>', methods=['DELETE'])
def delete_person(name):
    # находим артиста в базе и возвращаем ошибку, если его нет
    user = Person.query.filter_by(name=name).first()

    if not user:
        return jsonify({'reason':'User not found'}), 400
    # удаляем запись
    db.session.delete(user)
    # сохраняем изменения
    db.session.commit()

    # возвращаем успешный ответ
    return jsonify({'success': True})

if __name__ == '__main__':
    # запускаем сервер
    app.run()