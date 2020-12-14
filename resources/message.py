from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

import consts
from models.message import MessageModel


class Messages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(consts.SENDER_ID,
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument(consts.RECEIVER_ID,
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()

        messages = MessageModel.get_chat_messages(data[consts.SENDER_ID],
                                                  data[consts.RECEIVER_ID])
        messages_json = [message.json() for message in messages]
        return sorted(messages_json, key=lambda x: x[consts.MESSAGE_ID])

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(consts.RECEIVER_ID,
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument(consts.CONTENT,
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        data = parser.parse_args()

        message = MessageModel(get_jwt_identity(),
                               data[consts.RECEIVER_ID],
                               data[consts.CONTENT],
                               datetime.utcnow())
        message.save_to_db()

        return message.json(), 201
