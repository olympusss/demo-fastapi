from sqlalchemy import *
from sqlalchemy.orm import *
from db import Base
from datetime import *


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name_tm = Column(String)
    name_ru = Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    subcategory = relationship('subCategory', back_populates='category')
    product = relationship('Product', back_populates='category')
    
    
    
class subCategory(Base):
    __tablename__ = 'sub_category'
    id = Column(Integer, primary_key=True, index=True)
    name_tm = Column(String)
    name_ru = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    category = relationship('Category', back_populates='subcategory')
    product = relationship('Product', back_populates='subcategory')
    
    

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    name_tm = Column(String)
    name_ru = Column(String)
    description_tm = Column(String)
    description_ru = Column(String)
    price = Column(Float)
    code = Column(String)
    discount = Column(Float)
    is_favourite = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    subcategory_id = Column(Integer, ForeignKey('sub_category.id'))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    category    = relationship('Category', back_populates='product')
    subcategory = relationship('subCategory', back_populates='product')
    image       = relationship('Image', back_populates='product')
    favourite = relationship('Favourites', back_populates='product')
    
    
    
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    token = Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    favourite = relationship('Favourites', back_populates='user')
    
    
class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True)
    img = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    product = relationship('Product', back_populates='image')
    
    
class Favourites(Base):
    __tablename__ = 'favourites'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship('Users', back_populates='favourite')
    product = relationship('Product', back_populates='favourite')
    