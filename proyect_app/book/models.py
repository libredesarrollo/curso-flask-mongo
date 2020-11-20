import mongoengine as models

from flask_mongoengine import BaseQuerySet

from flask_mongoengine.wtf import model_form

class Category(models.Document):
    #_id = models.ObjectIdField()
    name = models.StringField(required=True, max_length=255)
    def __str__(self):
        return self.name

class Dimention(models.EmbeddedDocument):
    x = models.IntField()
    y = models.IntField()
    z = models.IntField()

class Address(models.EmbeddedDocument):
    direction = models.StringField()
    country = models.StringField(max_length = 20)

class Tag(models.Document):
    #_id = models.ObjectIdField()
    name = models.StringField(required=True, max_length=255)
    def __str__(self):
        return self.name

class Book(models.Document):
    _id = models.ObjectIdField()
    name = models.StringField(required=True, max_length=255)
    content = models.StringField(required=True)

    category = models.ReferenceField(Category)
    dimention = models.EmbeddedDocumentField(Dimention)
    addresses = models.EmbeddedDocumentListField(Address)
    tags = models.ListField(models.ReferenceField(Tag))

    meta = { 'queryset_class': BaseQuerySet}

    def __str__(self):
        return self.name

    def setByForm(self, form, addressForm):
        self.name = form.name.data
        self.content = form.content.data
        self.category = form.category.data
        
        #self.dimention = form.dimention.data
        self.dimention = Dimention(x=form.dimention.x.data, y=form.dimention.y.data, z=form.dimention.z.data)
        print(form.tags.data)
        self.addresses.append(Address(country=addressForm.country.data, direction=addressForm.direction.data))
        self.tags = form.tags.data


BookForm = model_form(Book)

AddressForm = model_form(Address)