import mongoengine as models
from flask_user import UserMixin
    
class User(models.Document, UserMixin):
    active = models.BooleanField(default=True)

    # User authentication information
    username = models.StringField(default='')
    password = models.StringField()

    # User information
    first_name = models.StringField(default='')
    last_name = models.StringField(default='')

    def __str__(self):
        return self.username

class UserBase(object):
    def __init__(self, id, username, password):
        self.id = str(id)
        self.username = username
        self.password = password
    
    def __str__(self):
      return f"User id: {self.id}"