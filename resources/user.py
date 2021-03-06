from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

import consts
from models.user import UserModel


class Users(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(consts.USER_ID,
                            type=str,
                            required=False,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()

        user_id = data[consts.USER_ID]

        if user_id:
            user = UserModel.get_user_by_id(data[consts.USER_ID])
            if user:
                return user.json(), 200
            return '', 200

        users = [user.json() for user in UserModel.get_all_users()]
        return users, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(consts.USER_ID,
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()
        user = UserModel.get_user_by_id(data[consts.USER_ID])
        if user:
            user.delete()

        return '', 200


class SignIn(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(consts.USER_ID,
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument(consts.NICKNAME,
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()
        user_id = data[consts.USER_ID]
        token = {
            'access_token': create_access_token(identity=user_id)
        }

        user = UserModel.get_user_by_id(user_id)
        if user is None:
            user = UserModel(user_id, data[consts.NICKNAME])
            user.save_to_db()
            return token, 201
        return token, 200
