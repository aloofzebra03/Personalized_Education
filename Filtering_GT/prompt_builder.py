from langchain.prompts import PromptTemplate

def build_filter_prompt(ongoing_concept: str,
                        section_name,
                        document_full_text: str) -> str:
    template = '''
        You are an AI assistant tasked with extracting the most relevant
        excerpt from a technical document.

        Ongoing Concept:
        {ongoing_concept}

        Section Name:
        {section_name}

        Full Document Text:
        {document_full_text}

        Instructions:
        - Identify the portion of the document that best matches the ongoing concept
        and the provided section parameters.
        - Return only the excerpt in paragraph form but ensure you include all relevant text.
        - Incase the document does not contain relevant information for the ongoing concept
        and section_name, return an empty string.
        '''.strip()

    prompt = PromptTemplate(
        input_variables=["ongoing_concept", "section_name", "document_full_text"],
        template=template
    )
    return prompt.format(
        ongoing_concept=ongoing_concept,
        section_name=section_name,
        document_full_text=document_full_text
    )