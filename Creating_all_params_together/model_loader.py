from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, MODEL_NAME

def load_llm():
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        api_key=GOOGLE_API_KEY,
        temperature=0.5,    
        top_p = 0.9,
        max_new_tokens=100000,
        transport='rest'
    )

# from huggingface_hub import InferenceClient
# from config import HF_API_TOKEN, MODEL_NAME

# class NewHuggingFaceLLM:
#     def __init__(self, model, token, temperature=0.5, top_p=0.9, max_new_tokens=100000):
#         self.client = InferenceClient(model=model, token=token)
#         self.temperature = temperature
#         self.top_p = top_p
#         self.max_new_tokens = max_new_tokens

#     def __call__(self, prompt, stop=None):
#         # Ensure the prompt is a string.
#         prompt_str = prompt if isinstance(prompt, str) else str(prompt)

#         # Call the text generation method.
#         outputs = self.client.text_generation(
#             prompt_str,
#             max_new_tokens=self.max_new_tokens,
#             temperature=self.temperature,
#             top_p=self.top_p
#         )

#         # Process the response based on its type.
#         # If the output is a list, check its first element.
#         if isinstance(outputs, list):
#             first_output = outputs[0]
#             if isinstance(first_output, dict) and 'generated_text' in first_output:
#                 return first_output['generated_text']
#             elif isinstance(first_output, str):
#                 return first_output

#         # If the output is a dict with the expected key.
#         elif isinstance(outputs, dict) and 'generated_text' in outputs:
#             return outputs['generated_text']
#         # If the output is already a string.
#         elif isinstance(outputs, str):
#             return outputs

#         # If none of the above conditions hold, raise an error.
#         raise ValueError("Unexpected response type from text_generation: " + str(type(outputs)))

# def load_llm():
#     return NewHuggingFaceLLM(
#         model=MODEL_NAME,
#         token=HF_API_TOKEN,
#         temperature=0.5,
#         top_p=0.9,
#         max_new_tokens=100000
#     )
