from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser

# class BatchAnswers(BaseModel):
#     """
#     Schema for batch answers returned by the LLM.
#     """
#     answers: List[str] = Field(
#         ...,
#         description="List of answers corresponding to each question in order"
#     )

# # Instantiate a parser that can be used in the chain's prompt
# # Use the `pydantic_object` parameter to match the library's expected signature
# parser = PydanticOutputParser(pydantic_object=BatchAnswers)

from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class SingleAnswer(BaseModel):
    answer: str = Field(..., description="The personalized answer")

parser = PydanticOutputParser(pydantic_object=SingleAnswer)

