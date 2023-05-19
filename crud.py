from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_
from models import Category, subCategory, Product, Users


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
        Product.name_tm, 
        Product.name_ru, 
        Product.description_tm, 
        Product.description_ru, 
        Product.price, 
        Product.code, 
        Product.discount,
        Category.name_tm.label('categoryNameTM'),
        Category.name_ru.label('categoryNameRU'),
        subCategory.name_tm.label('subCategoryNameTM'),
        subCategory.name_ru.label('subCategoryNameRU'),
    )\
    .join(Category, Category.id == Product.category_id)\
    .join(subCategory, subCategory.id == Product.subcategory_id)
    
    if category_id:
        result = result.filter(Product.category_id == category_id)
    if subcategory_id:
        result = result.filter(Product.subcategory_id == subcategory_id)
    result = result.all()
    return result



def signUp(req, db: Session):
    user = db.query(Users).filter(
        or_(
            Users.email == req.email,
            Users.username == req.username
        )
    ).first()
    if user:
        return False
    new_add = Users(**req.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return True


def signIn(req, db: Session):
    user = db.query(Users).filter(
        and_(
            or_(
                Users.email == req.email,
                Users.username == req.email
            ),
            Users.password == req.password
        )
    ).first()
    if user:
        return True
    
    
def read_users(db: Session):
    return db.query(Users.id, Users.email, Users.username).all()