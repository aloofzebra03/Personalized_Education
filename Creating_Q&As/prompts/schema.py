from pydantic import BaseModel
from typing import List

class QAPair(BaseModel):
    question: str
    answer: str

class QABatch(BaseModel):
    __root__: List[QAPair]
