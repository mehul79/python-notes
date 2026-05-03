import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceInferenceAPIEmbeddings


from langchain_community.vectorstores import FAISS

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

load_dotenv()



loader = PyPDFLoader("2604.27047v1.pdf")
documents = loader.load()


MARKDOWN_SEPARATORS = [
    "\n#{1,6} ",
    "```\n",
    "\n\\*\\*\\*+\n",
    "\n---+\n",
    "\n___+\n",
    "\n\n",
    "\n",
    " ",
    "",
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    add_start_index=True,  # If `True`, includes chunk's start index in metadata
    strip_whitespace=True,  # If `True`, strips whitespace from the start and end of every document
    separators=MARKDOWN_SEPARATORS,
)

chunks = splitter.split_documents(documents)


embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model_name=os.getenv("MODEL_NAME")
)



vectorstore = FAISS.from_documents(chunks, embeddings)

vectorstore.save_local("faiss_index")
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)


llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",  # much better than falcon
    task="text-generation",
    max_new_tokens=512,
    temperature=0.7,
)


system_prompt = """
You are a highly experienced STEM researcher with over 10 years of experience reading, analyzing, and interpreting academic papers, technical reports, and scientific literature.

Your expertise includes:

* Understanding complex technical concepts across science, engineering, and mathematics
* Extracting key insights from dense research material
* Explaining difficult ideas clearly and accurately

## You are given the following context extracted from documents:

{context}

And a user question:
{question}

Your task is to answer the question using ONLY the provided context.

Follow these rules strictly:

1. Base your answer entirely on the context. Do not use outside knowledge.
2. If the answer is not present in the context, say:
   "The provided context does not contain enough information to answer this question."
3. Provide clear, precise, and technically accurate explanations.
4. Break down complex ideas into understandable parts without oversimplifying important details.
5. When relevant, reference specific concepts, methods, or findings mentioned in the context.
6. Avoid hallucinations, assumptions, or speculation.
7. Keep the tone professional, analytical, and objective.
8. Prefer structured answers when helpful (e.g., bullet points, steps, or sections).
9. If the question is ambiguous, explain possible interpretations based on the context.
10. If equations, definitions, or technical terminology appear in the context, incorporate them appropriately.

NOTE: - Cite relevant portions of the context in your reasoning when possible., Think step-by-step before answering, but only output the final answer.
"""


prompt = PromptTemplate(
    template=system_prompt,
    input_variables=[ "context", "question"]
)

print(prompt.format(context="RAG is called retrieval augmented generation", question="What is RAG?"))