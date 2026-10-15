
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


if load_dotenv is not None:
    load_dotenv()

DOCUMENT_PATH = Path(__file__).parent / "technova_policy.txt"

QUESTIONS = [
    "How many paid annual leave days does a full-time employee receive per year?",
    "An employee wants to work remotely on Wednesday and take leave on Friday. "
    "What do the company policies say about these two requests?",
    "What is the company's parental leave policy?",
]


def load_document():
    if not DOCUMENT_PATH.is_file():
        raise FileNotFoundError(
            f"Could not find {DOCUMENT_PATH.name}. "
            "Place it in the same folder as this Python file."
        )

    documents = TextLoader(
        str(DOCUMENT_PATH),
        encoding="utf-8",
    ).load()

    if not documents or not documents[0].page_content.strip():
        raise ValueError(f"{DOCUMENT_PATH.name} is empty.")

    return documents


def build_rag():
    if not os.getenv("NVIDIA_API_KEY"):
        raise ValueError(
            "Missing NVIDIA_API_KEY. Set it in your terminal with: "
            "export NVIDIA_API_KEY='your_key_here'\n"
            "Or create a .env file containing: NVIDIA_API_KEY=your_key_here"
        )

    documents = load_document()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_documents(chunks, embeddings)

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    prompt = ChatPromptTemplate.from_template(
        """You are a policy assistant for TechNova Solutions.
Answer using only the policy context below.
Do not invent or assume policy details.
If the context does not contain the requested information, say:
"The provided document does not specify this policy."
Include relevant deadlines and approval requirements.

Context:
{context}

Question: {question}

Answer:"""
    )

    model = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
    temperature=0,
)

    chain = prompt | model | StrOutputParser()

    return retriever, chain


def answer_question(question, retriever, chain):
    retrieved_documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    return chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )


def main():
    retriever, chain = build_rag()

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"Question {number}: {question}")
        print(f"Answer: {answer_question(question, retriever, chain)}")
        print()


if __name__ == "__main__":
    main()


# Sample outputs based on the policy document:
#
# Question 1:
# Every full-time employee receives 18 paid annual leave days per calendar
# year. Requests must be submitted to the manager at least 3 calendar days
# before the requested leave date. Approval depends on the manager's
# confirmation.
#
# Question 2:
# Remote work is permitted on Wednesdays and Fridays. The employee must
# email their manager at least one working day in advance and obtain
# approval for remote work. Annual leave must be requested at least
# 3 calendar days in advance and requires manager confirmation.
#
# Question 3:
# The provided document does not specify this policy.
#
# These are sample outputs. Verify them against your actual run.
