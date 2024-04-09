from dotenv import load_dotenv
import os
from bson import ObjectId

from .models import Student

from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

client = AsyncIOMotorClient(os.getenv('MONGODB_CONNECTION_URI'))
database = client.StudentList
collection = database.get_collection("student") 

async def fetch_students(country : str|None = None, age : int|None = None):
    cursor = collection.find({})
    student_list = [Student(**document) async for document in cursor]
    if country:
        student_list=list(filter(lambda student: country in student.address.country ,student_list))
    if age:
        student_list=list(filter(lambda student: student.age >= age ,student_list))
    return [
        {
            "name":student.name,
            "age":student.age
        } for student in student_list
    ]

async def create_student(student: Student):
    document = student.model_dump()   
    res=await collection.insert_one(document)
    return str(res.inserted_id)

async def fetch_student_by_id(id:str):
    cursor = await collection.find_one({"_id": ObjectId(id)})
    student = Student(**cursor) # type: ignore
    return student

async def update_student_by_id(id:str,student: Student):
    
    data = student.model_dump(exclude_unset=True,exclude_none=True)
    data["address"] = student.address.model_dump(exclude_unset=True,exclude_none=True)
    result = await collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    return result

async def delete_student_by_id(id:str):
    res = await collection.find_one_and_delete({"_id": ObjectId(id)})
    if res is not None:
        return True
    else:
        return False
    
