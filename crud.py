from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_
from models import Category, subCategory, Product, Users, Image
<<<<<<< HEAD
from upload_depends import upload_image, delete_uploaded_image
=======
from upload_depends import upload_image
>>>>>>> 06e9ee5133e0225aab3595ded747c1ae3764ba48


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
    new_add = Users(
        email = req.email,
        password = req.password,
        username = req.username
    )
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



def create_img(id, file, db: Session):
    uploaded_file_name = upload_image('product', file)
    new_add = Image(
        img = uploaded_file_name,
        product_id = id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
<<<<<<< HEAD
    return new_add


def delete_img(id, db: Session):
    image = db.query(Image).filter(Image.id == id).first()
    if image.img:
        delete_uploaded_image(image_name=image.img)
        db.query(Image).filter(Image.id == id)\
            .delete(synchronize_session=False)
        db.commit()
    return True
=======
    return new_add
>>>>>>> 06e9ee5133e0225aab3595ded747c1ae3764ba48
