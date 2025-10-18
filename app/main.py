from fastapi import FastAPI, Depends, HTTPException, Form, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import uuid

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# setup to serve HTML templates
templates = Jinja2Templates(directory="templates")

# get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# serve HTML frontend
@app.get("/")
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# handle form & file uploads
@app.post("/requests/", response_model=schemas.Request, status_code=201)
def create_new_request_from_form(
    db: Session = Depends(get_db),
    customer_name: str = Form(...),
    text_request: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None)
):
    """
    create new customer request from form, save audio
    """
    file_path = None
    if audio_file and audio_file.filename:
        # make unique filename
        unique_id = uuid.uuid4()
        file_extension = audio_file.filename.split(".")[-1]
        unique_filename = f"{unique_id}.{file_extension}"
        file_path = f"uploads/{unique_filename}"

        # save file in uploads
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

    request_data = schemas.RequestCreate(customer_name=customer_name, request_text=text_request)
    return crud.create_request(db=db, request=request_data, audio_file_path=file_path)


@app.get("/requests/", response_model=List[schemas.Request])
def read_requests(status: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requests = crud.get_requests(db, status=status, skip=skip, limit=limit)
    return requests


@app.get("/requests/{request_id}", response_model=schemas.Request)
def read_request(request_id: int, db: Session = Depends(get_db)):
    db_request = crud.get_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@app.get("/requests/{request_id}/audio")
def stream_audio(request_id: int, db: Session = Depends(get_db)):
    """
    Streams the audio file associated with a specific request.
    """
    db_request = crud.get_request(db, request_id=request_id)
    if not db_request or not db_request.audio_file_path:
        raise HTTPException(status_code=404, detail="Request exists, but has no associated audio file.")
    
    return FileResponse(path=db_request.audio_file_path, media_type="audio/mpeg")


@app.post("/requests/{request_id}/solutions", response_model=schemas.Solution, status_code=201)
def create_solution(request_id: int, solution: schemas.SolutionCreate, db: Session = Depends(get_db)):
    """
    Submits a new solution for a specific request.
    """
    db_request = crud.get_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return crud.create_solution_for_request(db=db, solution=solution, request_id=request_id)


@app.put("/requests/{request_id}/close")
def close_a_request(request_id: int, db: Session = Depends(get_db)):
    """
    Closes a request, marking it as resolved.
    """
    db_request = crud.get_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    crud.close_request(db, request_id=request_id)
    return {"message": "Request has been closed."}
