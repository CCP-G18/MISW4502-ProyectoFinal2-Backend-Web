from app.models.user_model import User
from app.core.database import db

class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create(user: User):
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update(user: User):
        db.session.commit()
        return user
