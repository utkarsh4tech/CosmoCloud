from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    city: str 
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

class PatchStudent(BaseModel):
    name: Optional[str]
    age: Optional[int]
    address: Optional[Address]

