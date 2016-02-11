from model import Model
from pydblite import Base
from flask import blueprints, request
from datetime import datetime
import random

app = blueprints.Blueprint('pet', __name__)

class Pet(Model):
    name = 'pet'
    base = Base('database/' + name + '.pdl')

    def create_db(cls):
        cls.base.create('owner_id', 'name', 'breed', 'price', 'age', 'gender')

    def insert_db(cls, request):
        return cls.db().insert(owner_id = request.form['user_id'],
                               name = request.form['name'],
                               breed = request.form['breed'],
                               price = request.form['price'],
                               age = request.form['age'],
                               gender = request.form['gender'])

    def update_db(cls, item, request):
        return cls.db().update(item, name = request.form['name'],
                               breed = request.form['breed'],
                               price = request.form['price'],
                               age = request.form['age'],
                               gender = request.form['gender'])

@app.route('/pet/', methods=['GET'])
def get_pets():
    return Pet.get_items(request)

@app.route('/pet/', methods=['POST'])
def post_pet():
    return Pet.post_item(request)

@app.route('/pet/<id>', methods=['GET'])
def get_pet(id):
    return Pet.get_item(id, request)

@app.route('/pet/<id>', methods=['PUT'])
def put_pet(id):
    return Pet.put_item(id, request)

@app.route('/pet/<id>', methods=['DELETE'])
def delete_pet(id):
    return Pet.delete_item(id, request)

if len(Pet.db()) == 0:
    for i in range(0, 50):
        id = Pet.db().insert(owner_id=random.choice(range(0, 10)),
                             name='name{}'.format(i),
                             breed='breed{}'.format(random.choice(range(0, 5))),
                             price='price{}'.format(i),
                             age='age{}'.format(random.choice(range(0, 25))),
                             gender=random.choice(['male', 'female']))
        print(Pet(id).json())
    Pet.db().commit()