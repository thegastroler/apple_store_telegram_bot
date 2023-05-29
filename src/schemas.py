from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int
    username: str

    class Config:
        orm_mode = True