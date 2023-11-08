from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix='/contacts',
    tags=['Contacts']
)

@router.get('/', response_model=schemas.ContactsOut, status_code=status.HTTP_200_OK)
def get_contract(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    contacts = db.query(models.Contact).all()
    return schemas.ContactsOut(
        contacts = contacts,
        message = 'Contacts retrieved successfully!',
        status = status.HTTP_200_OK
    )

@router.get('/{id}', response_model=schemas.ContactOut, status_code=status.HTTP_200_OK)
def get_contract(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not contact:
        return schemas.ContactOut(
            status = status.HTTP_404_NOT_FOUND,
            message = 'Contact not found!'
        )
    return schemas.ContactOut(
        **contact.__dict__,
        status = status.HTTP_200_OK,
        message = 'Contact retrieved successfully!'
    )
