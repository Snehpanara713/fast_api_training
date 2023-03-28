from fastapi import FastAPI,Depends,HTTPException
from database import Base,SessionLocal,engine,func
from models import School,Student
from sqlalchemy.orm import Session 
from pydantic import BaseModel
from fastapi.responses import JSONResponse
# from fastapi_pagination import Page,add_pagination,paginate



# from typing import List 
# import sqlite3

Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# this is not student its a school.
class SchoolSchema(BaseModel):
    
    Name:str
    Address:str
    ContactNo:str
    class Config:
        orm_mode=True   # dictonary to convert json formet
    
class Student_Schema(BaseModel):
    FullName:str
    Std:int
    Division:str
    MobileNo:str
    SchoolId:int
    
    class Config:
        orm_mode=True   
        

@app.post("/insert",response_model=SchoolSchema,tags=["insert school"])
def create_school(school:SchoolSchema,db:Session=Depends(get_db)):
    u=School(Name=school.Name,Address=school.Address,ContactNo=school.ContactNo)
    db.add(u)
    db.commit()
    return u

@app.put("/update",tags=["update school"])
def update_school(s_id:int,school:SchoolSchema,db:Session=Depends(get_db)):
    try:
        # print(school)
        u=db.query(School).filter(School.id==s_id).first()
        print(u)
        u.Name=school.Name
        u.Address=school.Address
        u.ContactNo=school.ContactNo
        db.add(u)
        db.commit()
        db.refresh(u)
        return u
    except:
          return HTTPException (status_code=404,detail="user not found")
      
@app.delete("/delete",response_class=JSONResponse,tags=["delete school"])
def delete_school(school_id:int,db:Session=Depends(get_db)):
    try:
        u=db.query(School).filter(School.id==school_id).first()
        db.delete(u)
        db.commit()
        # db.refresh(u)
        return{f"user of id {school_id}"}
    except:
        return HTTPException(status_code=404,detail="user not found")


@app.get("/view",response_model=list[SchoolSchema],tags=["view school"])
def get_data(db:Session=Depends(get_db)):
    return db.query(School).all()


@app.post("/add_student",response_model=Student_Schema,tags=["insert student"])
def create_student(student:Student_Schema,db:Session=Depends(get_db)):
    # x=student(FullName=student.FullName,Std=student.Std,Division=student.Division,MobileNo=student.MobileNo)
    # print(student)
    db_student=Student  (FullName=student.FullName,Std=student.Std,Division=student.Division,MobileNo=student.MobileNo,SchoolId=student.SchoolId)
    print(db_student)
    db.add(db_student)
    db.commit()
    # db.refresh(db_student)
    return db_student 


@app.put("/update student",tags=["update student"])

def update_student(student_id:int,student:Student_Schema,db:Session=Depends(get_db)):
    try:
        x=db.query(Student).filter(Student.id==student_id).first()
        x.FullName=student.FullName
        x.Std=student.Std
        x.Division=student.Division
        x.MobileNo=student.MobileNo
        x.SchoolId=student.SchoolId
        db.commit()
        db.add(x)
        db.refresh(x)
        return x
    except:
         return HTTPException (status_code=404,detail="student not found")
     
     
@app.delete("/delete student",response_class=JSONResponse,tags=["delete student"])
def delete_student(student_id:int,db:Session=Depends(get_db)):
    try:
        s=db.query(Student).filter(Student.id==student_id).first()
        print(s)
        db.delete(s)
        db.commit()
        # db.refresh(s)
        return{f"user of id {student_id}"}
    except:
        return HTTPException(status_code=404,detail="student not found")
    
@app.get("/view",response_model=list[Student_Schema],tags=["view student"])
def get_student(db:Session=Depends(get_db)):
     return db.query(Student).all() #badho data malse
        
    

# @app.get("/join_table",)

# def get_join_student(db:Session, student_id:int):
#     return db.query(Student).join(School,School.SchoolId == Student.Id)

# def get_plan_studentID(student_id:int,db:Session=Depends(get_db)):
#     db_workout_plan=get_join_student(db,student_id=student_id)
    
#     if db_workout_plan is None:
#         raise HTTPException(status_code=404, detail="sorry.. no workoutplans found ..")
#     return [Student_Schema.from_orm(v)for v in db.query(...)]

@app.get('/join',tags=["join table"])
async def get_join(db:Session=Depends(get_db)):
    return db.query(Student,School).filter(Student.SchoolId, School.id).all()

    # lst = []
    # for std, schl in db.query(Student,School).filter(Student.SchoolId, School.id).all():
    #     lst.append({std.id,schl.SchoolId})
        
    # return lst
    
    # # return db.query(Student,School).filter(Student.SchoolId, School.id).all()
    # # return db.query(Student,School).filter(School.Name,Student.Std).all()
    
    # conn=sqlite3.connect('my_database.db')
    # xy= conn.execute"(SELECT Schools.Name, Students.FullName FROM Schools LEFT JOIN Students ON Schools.id = Students.id WHERE Students.id=1)"
    # # x=conn.execute("SELECT*FROM Schools LEFT JOIN Students ON Schools.ID = Students.ID WHERE Students.ID=1")
    # x=conn.execute(SELECT  Students.*,Schools.Name as SchoolName FROM Schools LEFT JOIN Students ON Schools.id = Students.SchoolId) 
    # conn.commit()
    # conn.close()
    # return {xy}
    
    
@app.get('/particular student',tags=["get detail"])
async def get_data(student_id: int,db:Session=Depends(get_db)):

# first method  --> running
    
    # query = (
    #     db.query(Student.Std,Student.FullName, School.Name)
    #     .select_from(Student)
    #     .join(School, Student.SchoolId == School.id)
    #     .filter(Student.id == student_id)
    # )
    # return query.first()


# second method --> running 

    query=db.query(Student.Std,Student.FullName,School.Name).join(School).filter(Student.id==student_id).first()
    return query


# third method --> running 

    query=db.query(Student.Std,School.Name).select_from(Student).join(School).filter(Student.id==student_id).first()
    # return query
    
@app.get('/get school',tags=["get school"])
async def get_school(school_id:int,db:Session=Depends(get_db)):
    # enter school id get student all student detail
    
    qery=db.query(Student.FullName,Student.Std,Student.Division,Student.MobileNo,School.Name).join(School).filter(School.id==school_id).first()

    return qery


# school id student count


@app.get('/count school and student',tags=["count std"])
async def count(school_id:int,db:Session=Depends(get_db)):
    # query=db.query(School.Name,func.count(Student.id).join(Student,School.id==school_id).group_by(School.Name))---> not working
    
    # query = db.query(School.Name, func.count(Student.id).label("student_count")).join(Student,Student.SchoolId == school_id).group_by(School.Name)---> not working
               
    query = db.query((School.Name).label("School_name"), func.count(Student.id).label("NoOfStudents"))\
                .join(Student, School.id == Student.SchoolId)\
                .filter(School.id==school_id)\
                .group_by(School.Name).first()
               
               
                
# SELECT Schools.Name, count(*) as student_count
# FROM Students  JOIN  Schools on Students.SchoolId=Schools.id 
# GROUP BY Schools.Name

    return query


@app.get('/search1',tags=["search"])
async def serach(student_name:str,school_id:str,db:Session=Depends(get_db)):
    result=db.query(Student).filter(Student.FullName.like(f"%{student_name}%")).filter(Student.SchoolId==school_id).all()
    return result


# school id=
# student name=


# ex raj

@app.get('/search',tags=["search 3 words and pagination "])
async def serach_three_word(student_name:str,school_id:int,page:int,page_size:int,db:Session=Depends(get_db)): #page:int,page_size:int
    # result=db.query(func.substr(Student.FullName,1,3),Student).filter(Student.FullName.like(f"%{student_name}%")).filter(Student.SchoolId==school_id)
    # result=db.query(Student.FullName),Student \
    # .filter(Student.FullName.like(f"{student_name}%")) \
    # .filter(Student.SchoolId==school_id) \
    # .offset((page-1)*page_size).limit(page_size).all()
    
# SELECT * 
# FROM Students
# JOIN Schools
# ON Students.SchoolId= Schools.id
# WHERE Students.FullName like 'a%'
# LIMIT 5
    
    print("hello ")
    total_count=db.query(Student).filter(Student.FullName.like(f"{student_name}%"),(Student.SchoolId==school_id)).count()
    
    # total_count= db.query(Student).filter(count(Student.SchoolId)).filter(Student.FullName.like(f"{student_name}%")).count()--> not working

    #total_count = db.query(func.count(Student).label("total")).filter(Student.FullName.like(f"{student_name}")).filter(Student.SchoolId == School.id)--> not working
    print(total_count)
 
    # SELECT COUNT(SchoolId) FROM Students WHERE FullName LIKE 'a%' AND SchoolId=6


    result= db.query(Student).filter(Student.FullName.like(f"{student_name}%"),(Student.SchoolId==school_id)).offset((page-1)*page_size).limit(page_size).all()
    
    # result=db.query(Student).filter(Student.FullName.like(f"%{student_name}%")).filter(Student.SchoolId==school_id).all()
    # print(result)
    
    return {"result":{"data":result,"total":total_count, "page_No":page,"page_size":page_size}}



# school ma bhanta 60kranu list and

