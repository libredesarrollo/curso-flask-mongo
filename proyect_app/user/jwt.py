
from .models import User, UserBase
from proyect_app import user_manager

def authenticate(username, password):
    print("_________________________________authenticate")
    user = User.objects(username=username).first()
    if user_manager.verify_password(password,user):
        userBase = UserBase(user.id, user.username, user.password)
        return userBase

def identity(payload):
    print("_________________________________identity")
    user_id = payload['identity']
    print(user_id)
    print(User.objects(id=user_id))
    return User.objects(id=user_id)