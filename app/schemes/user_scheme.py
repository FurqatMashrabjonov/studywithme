from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateDto(BaseModel):
    name: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserPublic(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)