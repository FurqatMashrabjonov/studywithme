from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class RegisterResponse(BaseModel):
    access_token: str

    model_config = {"from_attributes": True}