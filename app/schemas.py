from pydantic import BaseModel, EmailStr
from typing import Optional

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class OurBaseModelOut(OurBaseModel):
    message: Optional[str] = None
    status: Optional[int] = None

class User(OurBaseModel):
    email: EmailStr
    password: str

class UserOut(OurBaseModelOut):
    id: Optional[int] = None
    email: Optional[EmailStr] = None

class Token(OurBaseModelOut):
    access_token: Optional[str] = None
    token_type: Optional[str] = None

class TokenData(OurBaseModel):
    id: Optional[int] = None


class ContactOut(OurBaseModelOut):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None

class ContactsOut(OurBaseModelOut):
    contacts: Optional[list[ContactOut]] = []
