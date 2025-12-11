from pydantic import BaseModel
from typing import Optional

class ConvertRequest(BaseModel):
    content: str
    template_type: str = "article"
    author: str = "Anonymous"

class ConvertResponse(BaseModel):
    latex_code: str
    status: str

class AIRequest(BaseModel):
    command: str  # "polish", "complete", "explain"
    text: str

class AIResponse(BaseModel):
    result: str
    status: str
