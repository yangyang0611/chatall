from pydantic import BaseModel
from fastapi import UploadFile, File

class NewUser(BaseModel):
    username: str
    password: str | None = None
    
class UpdateUser(BaseModel):
    level: int | None = None
    room: int | None = None
    roomAdmin: int | None = None
    
class User(BaseModel):
    id: int
    name: str
    password: str
    level: int
    room: int

class new_v2_user_profile(BaseModel):
    name: str
    password: str
    email: str | None = None
    profile_picture: str | None = None # imugur link
    caption: str | None = None
    country: str | None = None

class v2_user(BaseModel):
    name: str
    password: str
    email: str | None = None
    profile_picture: str | None = None # imugur link
    caption: str | None = None
    friend_code: str | None = None
    country: str | None = None
    num_photos_uploaded: int | None = None

class user_picture(BaseModel):
    user_id: int
    url: str 
    picture: UploadFile = File(...)