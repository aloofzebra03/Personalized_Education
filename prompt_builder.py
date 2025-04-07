from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema import StudentProfile

parser = PydanticOutputParser(pydantic_object=StudentProfile)

prompt = PromptTemplate(
    template="""You are a school counselor. Generate a synthetic student profile with the following fields 
    ensuring that all the fields are filled up logically and do not conflict with each other.Ensure that the output is
    strictly in json format only.Respond Only with the json object and nothing else.:
{format_instructions}

""",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

__all__ = ["prompt", "parser"]
