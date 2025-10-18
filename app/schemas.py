from pydantic import BaseModel
from typing import List, Optional

#Solution Schemas
class SolutionBase(BaseModel):
    volunteer_name: str
    solution_text: str

class SolutionCreate(SolutionBase):
    pass

class Solution(SolutionBase):
    id: int
    request_id: int

    class Config:
        from_attributes = True

# Request Schemas
class RequestBase(BaseModel):
    customer_name: str
    request_text: Optional[str] = None

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int
    status: str
    audio_file_path: Optional[str] = None # Added this line
    solutions: List[Solution] = []

    class Config:
        from_attributes = True
