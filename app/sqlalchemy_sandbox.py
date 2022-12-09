#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'),
        UniqueConstraint(
            'email',
            name='unique_email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12'))
    
    Index('index_name', 'name')

    id = Column(Integer()) # primary_key=True not needed because of line 16 PrimaryKeyConstraint
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())
    
    # repr is short for representation
    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # use 'Session' class to create 'session' object
    session = Session()
    
    # create a Student object
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )
    
    # generate a statement to include in the session's transaction
    session.add(albert_einstein)
    # execute all statements in the transaction and saves any changes to the database
    session.commit()
    # session.commit() will also update your Student object with a id
    print(f"New student ID is {albert_einstein.id}.")
    
    
    
    
    ######    -----    #####   SAVING MULTIPLE INSTANCES    ######     ------    #####
    
    # If we want to save multiple new records in a single line of code, we can use the session's bulk_save_objects()
    
    # alan_turing = Student(
    #     name="Alan Turing",
    #     email="alan.turing@sherborne.edu",
    #     grade=11,
    #     birthday=datetime(
    #         year=1912,
    #         month=6,
    #         day=23
    #     ),
    # )
    
    # create session, student objects
        
    # session.bulk_save_objects([albert_einstein, alan_turing])
    # session.commit()
    
    # This code alone will return:
    
    # python app/sqlalchemy_sandbox.py
    # => New student ID is None.
    # => New student ID is None.
    
    # bulk_save_objects() does not associate the records with the session, so we don't update our records' IDs
    
    # students = session.query(Student)
    # print([student for student in students])
    # => [Student 1: Albert Einstein, Grade 6, Student 2: Alan Turing, Grade 11]
    
    # We would see the same output using the all() instance method
    # students = session.query(Student).all()
    # print(students)
    # => [Student 1: Albert Einstein, Grade 6, Student 2: Alan Turing, Grade 11]
    
    
    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")
    
    # Selecting only certain columns
    
    ######    -----    #####   SAVING MULTIPLE INSTANCES    ######     ------    #####