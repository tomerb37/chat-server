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
        sender_messages = cls.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).all()
        receiver_messages = cls.query.filter_by(sender_id=receiver_id, receiver_id=sender_id).all()
        messages = [message.json() for message in sender_messages]
        messages.extend([message.json() for message in receiver_messages])
        return sorted(messages, key=lambda x: x['id'])
    
    def json(self):
        return {
            'id': self.message_id,
            'senderId': self.sender_id,
            'receiverId': self.receiver_id,
            'content': self.content,
            'creationDate': self.creation_date.strftime('%c UTC')
        }
