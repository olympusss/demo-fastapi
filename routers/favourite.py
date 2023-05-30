from fastapi import *
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud

favourite_router = APIRouter()

@favourite_router.post('/favourite/{product_id}', dependencies=[Depends(HTTPBearer())])
def add_favourite(product_id: int, header_param: Request, db: Session = Depends(get_db)):
    try:
        result = crud.create_favourite(product_id, header_param, db)
        if result:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED, 
                content={'result': 'Successfully added to favourites'})
        else:
            return JSONResponse(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, 
                content={'result': 'This user not found'})
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Something went wrong')
    
    
    
@favourite_router.get('/favourite', dependencies=[Depends(HTTPBearer())])
def add_favourite(header_param: Request, db: Session = Depends(get_db)):
    try:
        result = crud.read_favourite(header_param, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED, 
                content=result)
        elif result == False:
            return JSONResponse(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, 
                content={'result': 'This user not found'})
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK, 
                content={'result': 'NO CONTENT'})
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Something went wrong')