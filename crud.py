from fastapi import Depends
from db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_
from models import Category, subCategory, Product, Users, Image, Favourites
from upload_depends import upload_image, delete_uploaded_image
from tokens import create_access_token, decode_token, check_token


def create_crud(req, model, db: Session):
    new_add = model(**req.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


def read_category(db: Session):
    result = db.query(Category).options(joinedload(Category.subcategory)).all()
    return result


def read_product(category_id, subcategory_id, db: Session):
    result = db.query(
        Product,
        Category.name_tm.label('categoryNameTm'),
        Category.name_ru.label('categoryNameRu'),
        subCategory.name_tm.label('subCategoryNameTm'),
        subCategory.name_ru.label('subCategoryNameRu'),
    ).options(joinedload(Product.image).load_only('img'))\
    .join(Category, Category.id == Product.category_id)\
    .join(subCategory, subCategory.id == Product.subcategory_id)
    
    if category_id:
        result = result.filter(Product.category_id == category_id)
    if subcategory_id:
        result = result.filter(Product.subcategory_id == subcategory_id)
    result = result.all()
    return result



def signUp(req, db: Session):
    if req.password == '' or \
        len(req.password) < 8 or \
            ' ' in req.password or \
                req.password != req.retype_password:
        return -1
    user = db.query(Users).filter(
        or_(
            Users.email == req.email,
            Users.username == req.username
        )
    ).first()
    if user:
        return False
    
    payload = {
        'username': req.username,
        'email': req.email,
        'password': req.password
    }
    token = create_access_token(payload)
    new_add = Users(
        email = req.email,
        password = req.password,
        username = req.username,
        token = token
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return True


def signIn(req, db: Session):
    user = db.query(Users.token).filter(
        and_(
            or_(
                Users.email == req.email,
                Users.username == req.email
            ),
            Users.password == req.password
        )
    ).first()
    if user:
        return user
    
    
def read_users(header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    username: str = payload.get('username')
    email: str = payload.get('email')
    password: str = payload.get('password')
    user = db.query(Users)\
        .filter(
            and_(
                Users.username == username, 
                Users.email == email, 
                Users.password == password
            )
        )\
            .first()
    if user:
        return db.query(Users).all()
    else:
        return False



def create_img(id, file, db: Session):
    uploaded_file_name = upload_image('product', file)
    new_add = Image(
        img = uploaded_file_name,
        product_id = id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


def delete_img(id, db: Session):
    image = db.query(Image).filter(Image.id == id).first()
    if image.img:
        delete_uploaded_image(image_name=image.img)
        db.query(Image).filter(Image.id == id)\
            .delete(synchronize_session=False)
        db.commit()
    return True


def read_user_id(username, password, db: Session):
    user = db.query(Users.id)\
        .filter(and_(Users.username == username, Users.password == password))\
            .first()
    if user:
        return user.id
    
    
def create_favourite(product_id, header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    username: str = payload.get('username')
    password: str = payload.get('password')
    user_id = read_user_id(username, password, db)
    if not user_id:
        return False
    new_add = Favourites(
        user_id = user_id,
        product_id = product_id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return True


def read_favourite(header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    username: str = payload.get('username')
    password: str = payload.get('password')
    user_id = read_user_id(username, password, db)
    if not user_id:
        return False
    favourites = db.query(Favourites).filter(Favourites.user_id == user_id).all()
    products = []
    for item in favourites:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        products.append(product)
    return products