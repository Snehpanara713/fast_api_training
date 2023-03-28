from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


# One is not the name proper name is Schools
class School(Base):
    __tablename__="Schools"
    id=Column(Integer,primary_key=True,index=True,unique=True)
    Name=Column(String(50))
    Address=Column(String(50))
    ContactNo=Column(String(50))
    
    owner=relationship("Student",back_populates="teacher")
    
class Student(Base):
    __tablename__="Students"
    id=Column(Integer,primary_key=True,index=True,unique=True)
    FullName=Column(String(50))
    Std=Column(Integer)
    Division=Column(String(50))
    MobileNo=Column(String(50))
    SchoolId=Column(Integer,ForeignKey('Schools.id'))
    
    teacher=relationship("School",back_populates="owner")
    
    
    # inner join
    # SELECT school.ID, student.FullName FROM school INNER JOIN student ON school.ID = student.School_ID;SchoolId=Column(Integer,ForeignKey("Schools.id"))
        
  
    
#     CREATE TABLE student (
#     ID int NOT NULL PRIMARY KEY,
#     FullName varchar(255),
#     Std int,
#     Division varchar(255),
#     Mo int,
#     FOREIGN KEY (School_ID) REFERENCES school(ID)
# );


# inner join
# SELECT school.ID, student.FullName FROM school INNER JOIN student ON school.ID = student.School_ID;


# left join
# SELECT school.Name, student.ID FROM school LEFT JOIN student ON school.ID = student.ID WHERE student.ID=1


# right join
# SELECT school.Address, student.School_ID FROM school RIGHT JOIN student ON student.ID = school.ID;

# full join

# SELECT school.Name, student.Std
# FROM school
# FULL OUTER JOIN student ON school.ID=student.ID
