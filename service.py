import oauth, pet, owner

from flask import Flask \
                , request \

app = Flask(__name__)
app.register_blueprint(pet.app)
app.register_blueprint(oauth.app)
app.register_blueprint(owner.app)

@app.route('/', methods=['GET'])
def index():
    return 'hello'

@app.route('/me', methods=['GET'])
def get_me():
    user_id = oauth.check_auth(request)
    #user_id = 0
    if user_id is None:
        return '', 401

    answer = owner.Owner(user_id).json()[0]
    pets = pet.Pet.db()(owner_id = user_id)
    for item in pets:
        answer += pet.Pet(item['__id__']).json()[0]
    return answer

if __name__ == '__main__':
    app.run(port=5050, debug=True, threaded=True)