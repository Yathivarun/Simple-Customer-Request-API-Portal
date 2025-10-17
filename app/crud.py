from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas

def get_request(db: Session, request_id: int):
    # Retrieve a single request by its ID, including its solutions
    return db.query(models.Request).filter(models.Request.id == request_id).first()

def get_requests(db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 100):
    # Retrieve a list of requests
    query = db.query(models.Request)
    if status:
        query = query.filter(models.Request.status == status)
    return query.offset(skip).limit(limit).all()

def create_request(db: Session, request: schemas.RequestCreate, audio_file_path: Optional[str] = None):
    # Create a new request record in the database
    db_request = models.Request(
        customer_name=request.customer_name,
        request_text=request.request_text,
        audio_file_path=audio_file_path
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def create_solution_for_request(db: Session, solution: schemas.SolutionCreate, request_id: int):
    # Create a new solution for a specific request
    db_solution = models.Solution(**solution.model_dump(), request_id=request_id)
    db.add(db_solution)
    db.commit()
    db.refresh(db_solution)
    return db_solution

def close_request(db: Session, request_id: int):
    # Update a request's status to 'closed'
    db_request = get_request(db, request_id=request_id)
    if db_request:
        db_request.status = "closed"
        db.commit()
        db.refresh(db_request)
    return db_request