from model import Model
from pydblite import Base
from flask import blueprints, request
from hashlib import sha256

app = blueprints.Blueprint('owner', __name__)

class Owner(Model):
    name = 'owner'
    base = Base('database/' + name + '.pdl')

    def create_db(cls):
        cls.base.create('login', 'password', 'name', 'email', 'phone', 'address')

    def insert_db(cls, request):
        return cls.db().insert(login=request.form['login'],
                               name=request.form['name'],
                               email=request.form['email'],
                               phone=request.form['phone'],
                               address=request.form['address'],
                               password=sha256(request.json['password'].encode('UTF-8')).hexdigest())

    def update_db(cls, item, request):
        return cls.db().update(item,
                               name=request.form['name'],
                               email=request.form['email'],
                               phone=request.form['phone'],
                               address=request.form['address'])

    def __init__(self, id):
        super().__init__(id)
        self.data.pop('password')

@app.route('/owner/', methods=['GET'])
def get_owners():
    return Owner.get_items(request)

@app.route('/owner/', methods=['POST'])
def post_owner():
    return Owner.post_item(request)

@app.route('/owner/<id>', methods=['GET'])
def get_owner(id):
    return Owner.get_item(id, request)

@app.route('/owner/<id>', methods=['PUT'])
def put_owner(id):
    return Owner.put_item(id, request)

@app.route('/owner/<id>', methods=['DELETE'])
def delete_owner(id):
    return Owner.delete_item(id, request)

if len(Owner.db()) == 0:
    for i in range(0, 100):
        id = Owner.db().insert(login='login{}'.format(i),
                               password=sha256('password'.encode('UTF-8')).hexdigest(),
                               name='name{}'.format(i),
                               email='login{}@example.com'.format(i),
                               phone='phone{}'.format(i),
                               address='address{}'.format(i))
        print(Owner(id).json())
    Owner.db().commit()

