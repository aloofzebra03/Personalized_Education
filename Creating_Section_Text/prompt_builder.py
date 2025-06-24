# prompt_builder.py

from Creating_Section_Text.schema import NextSectionChoice

_PROMPT = """
You are an AI tutor. Given this NextSectionChoice schema:
{model_schema}

Current section parameters for the current student:
{params}

Ongoing concept:
{concept}

Use these document excerpts as a base to build the next section of the concept:
{docs}

Generate the section content tailored to the student according to the given section parameters keeping in mind the min and max values from the schema.
Note: The section_name given to you in the section parameters is the name of the section that you need to generate content for.That is the next_section that the student is going to learn about.
Also ensure that you give only the section content in the output and nothing else.
Be concise and clear in your response, focusing on the key points relevant to the ongoing concept.

"""

def build_prompt(ongoing_concept: str, section_params: NextSectionChoice, docs: list):
    return _PROMPT.format(
        model_schema = NextSectionChoice.model_json_schema(),
        params       = section_params.model_dump_json(),
        concept      = ongoing_concept,
        docs         = "\n\n".join(d.page_content for d in docs)
    )
