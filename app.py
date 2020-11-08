from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.message import Messages
from resources.user import Users


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

api.add_resource(Messages, '/messages')
api.add_resource(Users, '/users')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
