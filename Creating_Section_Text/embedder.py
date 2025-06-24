import os
from Creating_Section_Text import config
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# make absolutely sure your key is set before any gRPC code loads:
os.environ["GOOGLE_API_KEY"]     = config.GOOGLE_API_KEY
os.environ["GOOGLE_API_USE_REST"] = "true"
os.environ["GRPC_DNS_RESOLVER"] = "native"


def get_embedder():
    print("Building Gemini embedder...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",  # <- NO "models/" prefix
        transport="rest",                    # <- HTTP/1.1 path only
        google_api_key=config.GOOGLE_API_KEY # <- explicit auth
    )
    # sanity check
    vec = embeddings.embed_query("hello, world!")
    print("Test Vector length:", len(vec))
    return embeddings

