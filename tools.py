from hashlib import md5
from typing import Type

from pydantic import ValidationError

from db import Session 
from models import Advertisement, User
from errors import HttpError 
from schema import AdCreation, AdPatching, UserCreation, UserPatching


def validate(input_data: dict, validation_model: Type[AdCreation] | Type[AdPatching] | Type[UserCreation] | Type[UserPatching]):
    try:
        model_item = validation_model(**input_data)
        return model_item.dict(exclude_none=True)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    

def get_ad(ad_id: int, session: Session):
    ad = session.get(Advertisement, ad_id)
    if ad is None:
        raise HttpError(404, 'Ad not found')
    return ad


def get_user(user_id: int, session: Session):
    user = session.get(User, user_id)
    if user is None: 
        raise HttpError(404, 'User not found')
    return user 


def hash_password(password: str):
    return md5(password.encode()).hexdigest()