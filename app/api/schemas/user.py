from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field("User Name", min_length=1, max_length=100)
    email: EmailStr
    password: str = Field("User Password", min_length=8, max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field("User Password", min_length=8, max_length=72)


