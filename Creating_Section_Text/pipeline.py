# pipeline.py

from Creating_Section_Text.model_loader    import get_llm
from Creating_Section_Text.retriever      import retrieve_docs
from Creating_Section_Text.prompt_builder import build_prompt
from Creating_Section_Text.schema         import NextSectionChoice
from Creating_Section_Text.vectorstore import build_vectorstore

def run_one(ongoing_concept: str, section_params: NextSectionChoice):
    docs   = retrieve_docs(ongoing_concept, section_params)
    for d in docs:
        print(f"Retrieved doc page_label: {d.metadata['page_label']}")

    prompt = build_prompt(ongoing_concept, section_params, docs)
    llm    = get_llm()
    out    = llm.invoke(prompt)
    return out.content

def ingest_and_build_store():
    vs = build_vectorstore()
    if vs is not None:
        print("Vector store built successfully.")

def run_one_gt(ongoing_concept: str, section_params: NextSectionChoice):
    docs   = retrieve_docs(ongoing_concept, section_params)
    answer = ""
    for d in docs:
        print(f"Retrieved doc page_label: {d.metadata['page_label']}")
        answer = answer + "-----------------------------------" + '\n' + f" # Retrieved doc page_label: {d.metadata['page_label']}" + '\n' +  d.page_content
    return answer
