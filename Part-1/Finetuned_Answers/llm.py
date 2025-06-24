
from transformers import pipeline
from langchain_community.llms import HuggingFaceEndpoint
from config import LLAMA_MODEL

def get_hf_pipeline():
    hf_pipe = pipeline(
        "text-generation",
        model=LLAMA_MODEL,
        device_map="auto",
        torch_dtype="auto",
        trust_remote_code=True,
        max_new_tokens=512,
    )
    return HuggingFaceEndpoint(pipeline=hf_pipe)

# llm.py
from langchain.llms import HuggingFaceEndpoint
from config import NGROK_URL  # see step C

# def get_remote_llm() -> HuggingFaceEndpoint:
    
#     return HuggingFaceEndpoint(
#         endpoint_url=f"{NGROK_URL}/generate",
#         input_key="prompt",
#         output_key="text",
#         headers={},
#         do_sample=False,            # sampling off (greedy)
#         max_new_tokens=512,         # limit on generation length
#         stop=["}"],   
#                 # empty unless you secure your endpoint
#     )

# llm.py
from langchain_community.llms import HuggingFaceEndpoint
from config import NGROK_URL

def get_remote_llm() -> HuggingFaceEndpoint:
    return HuggingFaceEndpoint(
        endpoint_url=f"{NGROK_URL}/generate",
        input_key="inputs",
        output_key="generated_text",
        headers={},              

        # Pass decoding params as top-level args:
        do_sample=True,          # enable sampling
        temperature=0.5,         # sampling temperature
        top_p=0.9,               # nucleus sampling cutoff
        max_new_tokens=512,      # max tokens to generate
        # stop=["}"],              # stop right after your JSON
    )

