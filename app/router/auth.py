from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Auth']
)

@router.post('/login', response_model = schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_in_db = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()
    
    if not user_in_db:
        return schemas.Token(
            status=status.HTTP_403_FORBIDDEN,
            message="Invalid Credentials!"
        )
    
    if not utils.verify_password(user_credentials.password, user_in_db.password):
        return schemas.Token(
            status=status.HTTP_403_FORBIDDEN,
            message="Invalid Credentials!"
        )
    
    data = {
        "user": {
            "id": user_in_db.id,
            "email": user_in_db.email
        }
    }
    
    access_token = oauth2.create_access_token(data = data)
    return schemas.Token(
        access_token = access_token,
        token_type = "bearer",
        status = status.HTTP_200_OK
    )
