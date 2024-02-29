from pydantic import BaseModel

class NewRoom(BaseModel):
    ownerId: int
    roomName: str
    descript: str
    limit: int
    
class Room(BaseModel):
    id: int
    name: str
    descript: str
    limit: int
    #owner: str