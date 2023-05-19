from fastapi import FastAPI
from db import Base, engine
from routers import *


app = FastAPI()


Base.metadata.create_all(engine)


app.include_router(authentication_router, tags=['Authentication'])
app.include_router(category_router, tags=['Category'])
app.include_router(subcategory_router, tags=['Sub-Category'])
app.include_router(product_router, tags=['Product'])
