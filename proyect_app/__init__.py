from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db" : 'testmongoflask'
}

app.config['SECRET_KEY'] = 'as54556ad4a56sd454d5gf56sd74f/8f56sd4f541ad45as4d4a5sd45a4sd6a'
app.config['USER_ENABLE_EMAIL'] = False
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
app.debug=True

db = MongoEngine(app)

from flask_user import UserManager
from proyect_app.user.models import User, UserBase
user_manager = UserManager(app, db, User)

# JWT
from flask_jwt import JWT
from proyect_app.user.jwt import authenticate, identity

jwt = JWT(app, authenticate, identity)

# controladores book
from proyect_app.book.controllers import bookBp
app.register_blueprint(bookBp)

# controladores user
from proyect_app.user.controllers import userBp
app.register_blueprint(userBp)

# restful Api
from flask_restful import Api
from proyect_app.rest.controllers import BookApi, BookApiId, CategoryBookApiId, TagAddBookApiId, TagRemoveBookApiId, AddressAddBookApiId, AddressRemoveBookApiId

api = Api(app) #, decorators=[csrf.exempt]
api.add_resource(BookApi, '/api/book')
api.add_resource(BookApiId, '/api/book/<string:id>')
api.add_resource(CategoryBookApiId, '/api/book/set_category/<string:id>')
api.add_resource(TagAddBookApiId, '/api/book/add_tag/<string:id>')
api.add_resource(TagRemoveBookApiId, '/api/book/remove_tag/<string:id>')
api.add_resource(AddressAddBookApiId, '/api/book/add_address/<string:id>')
api.add_resource(AddressRemoveBookApiId, '/api/book/remove_address/<string:id>')

