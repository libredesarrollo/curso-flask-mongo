from flask import Response, request, jsonify
from flask_restful import Resource, fields, marshal_with, reqparse

from proyect_app.book.models import Book, Category, Address, Tag, Dimention, Address

cate_tag_fields = {
    '_id': fields.String,
    'name' : fields.String,   
}

address_fields = {
    'direction': fields.String,
    'country' : fields.String,   
}

dimention_fields = {
    'x': fields.Integer,
    'y': fields.Integer,
    'z': fields.Integer
}

resource_fields = {
    '_id': fields.String,
    'name' : fields.String,
    'content': fields.String,
    #'category': fields.String,
    'category': fields.Nested(cate_tag_fields),
    'tags': fields.Nested(cate_tag_fields),
    #'tags': fields.String,
    'addresses': fields.Nested(address_fields),
    'dimention': fields.Nested(dimention_fields),
}

pipes = [
    {'$lookup': {'from': Category._get_collection_name(),
                    'localField': 'category',
                    'foreignField': '_id',
                    'as': 'category'}},
    {'$unwind': "$category"},
    {'$lookup': {'from': Tag._get_collection_name(),
                    'localField': 'tags',
                    'foreignField': '_id',
                    'as': 'tags'}},
    #{'$unwind': "$tags"},
]

class BookApi(Resource):

    @marshal_with(resource_fields, envelope="books")
    def get(self):
        #books = Book.objects.to_json()
        books = Book.objects.aggregate(*pipes)
        books = list(books)

        return books
        print(books)

        #return Response(books, mimetype="application/json", status=200)

    @marshal_with(resource_fields, envelope="book")
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('name',required=True, help="No mandastes el nombre")
        parser.add_argument('content',required=True, help="No mandastes el contenido")
        parser.add_argument('category_id',required=True, help="No mandastes la categoría")
        parser.add_argument('dimention-x',required=True, help="No mandastes las dimenciones x")
        parser.add_argument('dimention-y',required=True, help="No mandastes las dimenciones y")
        parser.add_argument('dimention-z',required=True, help="No mandastes las dimenciones z")

        args = parser.parse_args()

        book = Book(name=args['name'], content=args['content'])

        category = Category.objects.get(pk=args['category_id'])
        book.category = category

        dimention = Dimention(x=args['dimention-x'], y=args['dimention-y'], z=args['dimention-z'])
        book.dimention = dimention

        book.save()

        print(book._id)
        print(book.pk)
        print(book)

        #book = Book.objects.get(_id=book.pk)
        book = Book.objects(_id=book.pk).aggregate(*pipes)
        #book = list(book)[0] if list(book) else None
        return list(book)[0]


class BookApiId(Resource):

    @marshal_with(resource_fields, envelope="book")
    def get(self,id):
        #book = Book.objects.get(_id=id).to_json()
        print(Book.objects(_id=id))
        book = Book.objects(_id=id).aggregate(*pipes)
        #print(list(book)[0])
        #book = 
        #print(book)
        return list(book)[0] 
        #return Response(book, mimetype="application/json", status=200)

    @marshal_with(resource_fields, envelope="book")
    def patch(self, id):
        
        parser = reqparse.RequestParser()
        parser.add_argument('name',required=True, help="No mandastes el nombre")
        parser.add_argument('content',required=True, help="No mandastes el contenido")
        parser.add_argument('category_id',required=True, help="No mandastes la categoría")
        parser.add_argument('dimention-x',required=True, help="No mandastes las dimenciones x")
        parser.add_argument('dimention-y',required=True, help="No mandastes las dimenciones y")
        parser.add_argument('dimention-z',required=True, help="No mandastes las dimenciones z")

        args = parser.parse_args()

        book = Book.objects.get(_id=id)

        book.name = args['name']
        book.content = args['content']

        category = Category.objects.get(pk=args['category_id'])
        book.category = category

        dimention = Dimention(x=args['dimention-x'], y=args['dimention-y'], z=args['dimention-z'])
        book.dimention = dimention

        book.save()

        print(book._id)
        print(book.pk)
        print(book)

        #book = Book.objects.get(_id=book.pk)
        book = Book.objects(_id=book.pk).aggregate(*pipes)
        #book = list(book)[0] if list(book) else None
        return list(book)[0]

    def delete(self, id):

        Book.objects(_id=id).delete()

        return {'msj':'ok'}


class CategoryBookApiId(Resource):

    @marshal_with(resource_fields, envelope="book")
    def patch(self, id): 
        
        parser = reqparse.RequestParser()
        parser.add_argument('category_id',required=True, help="No mandastes la categoría")

        args = parser.parse_args()

        book = Book.objects.get(_id=id)
        category = Category.objects.get(pk=args['category_id'])
        book.category = category

        book.save()

        #book = Book.objects.get(_id=book.pk)
        book = Book.objects(_id=book.pk).aggregate(*pipes)
        #book = list(book)[0] if list(book) else None
        return list(book)[0]

class TagAddBookApiId(Resource):

    @marshal_with(resource_fields, envelope="book")
    def patch(self, id): 
        
        parser = reqparse.RequestParser()
        parser.add_argument('tag_id',required=True, help="No mandastes el tag")

        args = parser.parse_args()

        book = Book.objects.get(_id=id)
        tag = Tag.objects.get(pk=args['tag_id'])
        book.tags.append(tag)

        book.save()

        #book = Book.objects.get(_id=book.pk)
        book = Book.objects(_id=book.pk).aggregate(*pipes)
        #book = list(book)[0] if list(book) else None
        return list(book)[0]

class TagRemoveBookApiId(Resource):

    @marshal_with(resource_fields, envelope="book")
    def delete(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('tag_id',required=True, help="No mandastes el tag")

        args = parser.parse_args()

        book = Book.objects.get(_id=id)

        tag = Tag.objects.get(pk=args['tag_id'])

        try:
            book.tags.remove(tag)
            book.save()
        except ValueError:
            pass

        books = Book.objects(_id=id).aggregate(*pipes)

        try:
            book = list(books)[0]
        except IndexError:
            return

        return book

class AddressAddBookApiId(Resource):

    @marshal_with(resource_fields, envelope="book")
    def patch(self, id): 
        
        parser = reqparse.RequestParser()
        parser.add_argument('direction',required=True, help="No mandastes la dirección")
        parser.add_argument('country',required=True, help="No mandastes el país")

        args = parser.parse_args()

        book = Book.objects.get(_id=id)
        address = Address(direction=args['direction'], country=args['country'])
        book.addresses.append(address)

        book.save()

        #book = Book.objects.get(_id=book.pk)
        book = Book.objects(_id=book.pk).aggregate(*pipes)
        #book = list(book)[0] if list(book) else None
        return list(book)[0]

class AddressRemoveBookApiId(Resource):

    @marshal_with(resource_fields, envelope="book")
    def delete(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('index', type=int, required=True, help="No mandastes el indice")

        args = parser.parse_args()

        book = Book.objects.get(_id=id)

        try:
            book.addresses.pop(args['index'])
            book.save()
        except IndexError:
            pass

        books = Book.objects(_id=id).aggregate(*pipes)

        try:
            book = list(books)[0]
        except IndexError:
            return

        return book