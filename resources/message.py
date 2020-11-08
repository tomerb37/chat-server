from datetime import datetime
from flask_restful import Resource, reqparse

from models.message import MessageModel


class Messages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('senderId',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('receiverId',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()

        return MessageModel.get_chat_messages(data['senderId'],
                                              data['receiverId'])


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('senderId',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('receiverId',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('content',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()

        message = MessageModel(data['senderId'],
                               data['receiverId'],
                               data['content'],
                               datetime.now())
        message.save_to_db()

        return message.json(), 201


class MessagesList(Resource):
    def get(self):
        return {'messages': [message.json() for message in MessageModel.query.all()]}
