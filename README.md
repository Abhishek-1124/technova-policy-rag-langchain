# TechNova Policy RAG Using LangChain

A Retrieval-Augmented Generation (RAG) system that answers employee questions using the TechNova Solutions policy document.

## Features

- Loads a Google Docs policy document using LangChain.
- Splits the document into overlapping text chunks.
- Generates text embeddings using OpenAI.
- Stores embeddings in a FAISS vector store.
- Retrieves the top 3 relevant chunks per question.
- Generates context-grounded answers using LangChain and an LLM.
- Handles questions about information missing from the source document.

## Tech Stack

- Python
- LangChain
- OpenAI embeddings and chat model
- FAISS
- Google Docs export endpoint

## Setup

1. Create and activate a Python virtual environment.
2. Install the dependencies listed in the project setup instructions.
3. Set the `OPENAI_API_KEY` environment variable.
4. Ensure the Google Doc is accessible to the script.
5. Run `python technova_rag.py`.

## Test Questions

1. How many paid annual leave days does a full-time employee receive per year?
2. An employee wants to work remotely on Wednesday and take leave on Friday. What do the company policies say about these two requests?
3. What is the company's parental leave policy?

## Expected Behavior

The system should answer policy questions using retrieved context and explicitly state when the document does not contain the requested information.

## Security

Never commit API keys, access tokens, or other secret credentials.
