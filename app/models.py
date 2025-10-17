from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    request_text = Column(String, nullable=True)
    audio_file_path = Column(String, nullable=True) # To store the path to the audio file
    status = Column(String, default="open") # Status can be 'open' or 'closed' [cite: 18]

    solutions = relationship("Solution", back_populates="request")

class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    solution_text = Column(String)
    volunteer_name = Column(String)
    request_id = Column(Integer, ForeignKey("requests.id")) # Links to the request it solves [cite: 19]

    request = relationship("Request", back_populates="solutions")