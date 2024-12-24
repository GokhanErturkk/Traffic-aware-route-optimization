from pydantic import BaseModel 

class CarInfo(BaseModel):
    citypoint:int
    velocity: int


class TargetNode(BaseModel):
    targetNode:str
    

