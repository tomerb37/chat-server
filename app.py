import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.message import Messages
from resources.user import Users, SignIn


app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tmp/test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'chat-app'
jwt = JWTManager(app)

api = Api(app)

api.add_resource(Messages, '/messages')
api.add_resource(Users, '/users')
api.add_resource(SignIn, '/signin')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
