from typing import Optional

from pydantic import BaseModel, validator 


class AdCreation(BaseModel):

    title: str
    description: str
    user_id: int


class AdPatching(BaseModel):

    title: Optional[str]
    description: Optional[str]


class UserCreation(BaseModel):

    email: str
    password: str

    @validator('password')
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError('password is too short')
        return value 
    

class UserPatching(BaseModel):
    
    email: Optional[str]
    password: Optional[str]

    @validator('password')
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError('password is too short')
        return value 