from pydantic import BaseModel
from pydantic import RootModel
from typing import List

class QAPair(BaseModel):
    question: str
    answer: str

class QABatch(RootModel[List[QAPair]]):
    pass
