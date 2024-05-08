from application.database import db
from flask_sqlalchemy import SQLAlchemy








'''roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

user_product=db.table('user_product',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('product_id', db.Integer(), db.ForeignKey('product.id')))       

product_image=db.table('product_image',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('product_id', db.Integer(), db.ForeignKey('product.id')))
                       
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Product(db.Model):
    __tablename__="product"
    product_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    name=db.Column(db.String(200),unique=True)
    description=db.Column(db.String(1000))
    price=db.Column(db.Integer)
    #images = db.relationship('Product', secondary=product_image, backref=db.backref('image', lazy='dynamic'))
    #users = db.relationship('User', secondary=user_product, backref=db.backref('products', lazy='dynamic'))
    images = db.relationship('Image', backref='product', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String, unique=False,nullable=False)
    email = db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    #address=db.Column(db.String,nullable=False)
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))
 
    #products = db.relationship('Product', secondary=user_product, backref=db.backref('users', lazy='dynamic'))
    products = db.relationship('Product', secondary=user_product,
                               primaryjoin=(user_product.c.user_id == id),
                               secondaryjoin=(user_product.c.product_id == Product.product_id),
                               backref=db.backref('users', lazy='dynamic'))



class Image(db.Model):
    __tablename__="image"
    image_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    url=db.column(db.String())
    product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id'))'''
    
   
# Association table for roles and users
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

# Association table for users and products
user_product = db.Table('user_product',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('product_id', db.Integer, db.ForeignKey('product.product_id')))

# Role model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# Product model
class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    images = db.relationship('Image', backref='product', lazy='dynamic')

# User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    products = db.relationship('Product', secondary=user_product,
                               backref=db.backref('users', lazy='dynamic'))

# Image model
class Image(db.Model):
    __tablename__ = "image"
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String())
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
