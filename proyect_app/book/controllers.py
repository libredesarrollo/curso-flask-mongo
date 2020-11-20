from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify

from proyect_app import app

from .models import Book, BookForm, Category, Dimention, Address, AddressForm, Tag

bookBp = Blueprint('book',__name__, url_prefix='/book')

@bookBp.route('/')
@bookBp.route('/<int:page>')
def index(page=1):
    #save_category()
    #save_tag()
    return get_list_paginate(page,BookForm(),AddressForm())

@bookBp.route('/add', methods=('GET', 'POST'))
def add():

    print(request.method)
    if request.method == 'GET':
        return redirect(url_for('book.index'))

    form=BookForm(request.form)
    addressForm=AddressForm(request.form)
    if request.method == 'POST' and form.validate():
        book = Book()
        book.setByForm(form, addressForm)
        book.save()
        #print(form.dimention.csrf_token)
        #print(form.csrf_token)
        #print("___-_")
        #del form.dimention.csrf_token
        #del form.csrf_token
        
        
        #form.save()
        return redirect(url_for('book.index'))

    if form.errors:
        print(form.errors)
        flash(form.errors,'danger')

    return get_list_paginate(1,form,addressForm)
    #return render_template('book/add.html', form=BookForm())

@bookBp.route('/update/<string:id>', methods=('POST',))
def update(id):
    book = Book.objects.get_or_404(_id=id)

    
    form=BookForm(request.form)
    addressForm=AddressForm(request.form)
    
    if request.method == 'POST' and form.validate() and addressForm.validate():
        #book.name = form.name.data
        #book.content = form.content.data
        #book.category = Category.objects.get(_id="5f78b8da62f91b4acd32553e")
        book.setByForm(form, addressForm)
        #book.addresses = [Address(direction="Dir Test", country="Venezuela"), Address(direction="Dir Test", country="Venezuela")]
        #book.addresses.append(Address(direction="Dir Test 2", country="España"))
        #book.category = Category.objects.get(pk="5f78b8da62f91b4acd32553e")
        #book.dimention = Dimention(x=2,y=7,z=9)

        #tag = Tag.objects.get(pk="5f79f50163859e02bfc52a75")
        #tag2 = Tag.objects.get(pk="5f79f50163859e02bfc52a76")
        #book.tags.append(tag)
        #book.tags.append(tag2)

        #book.tags = [tag, tag2]
        
        print(book.category)
        book.save()
        return redirect(url_for('book.index'))
    return get_list_paginate(1,form,addressForm)

@bookBp.route('/delete/<string:id>', methods=('POST',))
def delete(id):
    Book.objects(_id=id).delete()
    return redirect(url_for('book.index'))

def get_list_paginate(page, form, formAddress):
    return render_template('book/index.html', books = Book.objects.paginate(page=page, per_page=10), form=form, formAddress=formAddress)


#------------Json

@bookBp.route('/get_detail_by_id/<string:id>')
def getDetailById(id):
    return jsonify(Book.objects.get(_id=id))


#------------Test

def save_category():
    category = Category(name="Cate 1")
    category.save()

    category = Category(name="Cate 2")
    category.save()

def save_tag():
    tag = Tag(name="Tag 1")
    tag.save()

    tag = Tag(name="Tag 2")
    tag.save()

def update_document():
    book = Book.objects.get_or_404(_id='5f6f2a0a4d4022fb13d980c6')
    book.name = "Harry Potter"
    book.content = "Libro con un final malo... :("
    book.save()
    book = Book.objects.get_or_404(_id='5f6f2a0a4d4022fb13d980c6')
    print(book.name)

def get_document_by_id():
    #book = Book.objects.get(_id='5f6e6984c518f9eb5b412909')
    book = Book.objects.get_or_404(_id='5f6f4b31c8be02ceb8437e8d')
    print(book._id)

def save_document():
    book = Book(name="GOT", content="Vientos de invierno")
    book.save()

def delete_document():
    book = Book(name="GOT", content="Vientos de invierno")
    book.save()
    print(book.pk)
    #book.delete()

    Book.objects(_id=book.pk).delete()
    #print(book.pk)
    #print(book._id)
    #book.delete() # si va a funcionar
    #book = Book.objects(_id=book.pk).delete()
    

def get_document():
    book = Book.objects(name="GOT").first()
    print(book._id)
    print(book.name)

def get_documents():
    books = Book.objects(name="GOT").all()
    print(books)