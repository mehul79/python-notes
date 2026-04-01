#using hugging face API
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="zai-org/GLM-4.7-Flash",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

result = model.invoke("what is the maths formula for compound interest?")

print(result.content)