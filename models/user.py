import consts
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Text, primary_key=True)
    nickname = db.Column(db.Text,
                         nullable=False)

    def __init__(self, user_id, nickname):
        self.user_id = user_id
        self.nickname = nickname

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user_by_id(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()

        if user:
            return user
        return

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    def json(self):
        return {
            consts.USER_ID: self.user_id,
            consts.NICKNAME: self.nickname
        }
