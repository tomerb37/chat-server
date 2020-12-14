import consts
from db import db


class MessageModel(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Text,
                          nullable=False)
    receiver_id = db.Column(db.Text,
                          nullable=False)
    content = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)

    def __init__(self, sender_id, receiver_id, content, creation_date):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.creation_date = creation_date
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_chat_messages(cls, sender_id, receiver_id):
        messages = cls.query.filter(
            ((cls.sender_id == sender_id) & (cls.receiver_id == receiver_id)) |
            (cls.sender_id == receiver_id) & (cls.receiver_id == sender_id)).all()
        return messages
    
    def json(self):
        return {
            consts.MESSAGE_ID: self.message_id,
            consts.SENDER_ID: self.sender_id,
            consts.RECEIVER_ID: self.receiver_id,
            consts.CONTENT: self.content,
            consts.CREATION_DATE: self.creation_date.strftime('%c UTC')
        }
