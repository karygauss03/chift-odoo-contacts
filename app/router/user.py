from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    
    if db_user:
        return schemas.UserOut(
            status = status.HTTP_400_BAD_REQUEST,
            message = 'Email already used'
        )
    
    try:
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
    except SQLAlchemyError as e:
        return schemas.UserOut(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="There is a problem, try again!"
        )
    return schemas.UserOut(
        **new_user.__dict__,
        status=status.HTTP_201_CREATED,
        message="User created successfully!"
    )
