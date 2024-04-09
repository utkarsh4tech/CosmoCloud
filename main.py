from fastapi import FastAPI, HTTPException, status

from application.data.database import (
    fetch_students, 
    create_student,
    fetch_student_by_id,
    update_student_by_id,
    delete_student_by_id
    )
from application.data.models import Student



def make_app(app=None):
    app = FastAPI(title="CosmoCloud Hiring Challenge")

    return app

app = make_app()

@app.get("/")
def app_root():
    return {"ping":"pong"}

@app.get(
        "/students",
        status_code= status.HTTP_200_OK, 
        description="""An API to find a list of students. 
        You can apply filters on this API by passing the
        query parameters as listed below.""",
        tags=["STUDENTS"]
)
async def get_students(country : str|None = None, age : int|None = None):
    res = await fetch_students(country,age)
    return {"data":res}

@app.post(
        "/students", 
        status_code= status.HTTP_201_CREATED, 
        description="""API to create a student in the system. 
        All fields are mandatory and required while creating the student in the system.""",
        tags=["STUDENTS"]
    )
async def post_student(student: Student):
    res= await create_student(student)
    if res:
        return  {"id":res}
    else:
        raise HTTPException(400,"Something Went Wrong")
    
@app.get(
        "/students/{id}",
        status_code= status.HTTP_200_OK,
        tags=["STUDENTS"]
    )
async def get_student(id:str):
    res= await fetch_student_by_id(id)
    return res

@app.patch(
    "/students/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""API to update the student's properties based on information provided. 
    Not mandatory that all information would be sent in PATCH,
    only what fields are sent should be updated in the Database.""",
    response_model_exclude_unset=True,
    tags=["STUDENTS"]
)
async def patch_student(id:str,student: Student):
    result = await update_student_by_id(id,student)
    if result is not None:
        return {}
    else:
        raise HTTPException(404,"Student Not Found")
    
@app.delete(
    "/students/{id}",
    status_code=status.HTTP_200_OK,
    description="API to Delete student",
    tags=["STUDENTS"]
)
async def delete_student(id:str):
    res = await delete_student_by_id(id)
    if res:
        return {}
    else:
        raise HTTPException(404,"Student Not Found")