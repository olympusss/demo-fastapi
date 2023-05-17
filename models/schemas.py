from pydantic import BaseModel


class BaseSchema(BaseModel):
    name_tm: str
    name_ru: str
    
    
class subCategorySchema(BaseSchema):
    category_id: int
    
    
class productSchema(subCategorySchema):
    description_tm: str
    description_ru: str
    price: float 
    code: str 
    discount: float
    subcategory_id: int
    