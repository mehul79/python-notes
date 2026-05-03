import os
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpointEmbeddings


os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_..."

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.7,
    max_tokens=1024,
)