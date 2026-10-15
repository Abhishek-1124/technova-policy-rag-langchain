# TechNova Policy RAG Using LangChain

A Retrieval-Augmented Generation (RAG) application that answers employee questions using the TechNova Solutions policy document.

## Features

- Loads `technova_policy.txt` from the same folder as the Python script.
- Splits the document into smaller text chunks.
- Generates embeddings locally using Hugging Face Sentence Transformers.
- Stores and searches embeddings using FAISS.
- Retrieves the three most relevant chunks for each question.
- Uses an NVIDIA-hosted language model to generate answers from the retrieved context.
- Instructs the model to state when the requested information is not available in the document.

## Tech Stack

- Python
- LangChain
- Hugging Face Sentence Transformers
- FAISS
- NVIDIA API Catalog

## Project Structure

```text
technova-policy-rag-langchain/
├── technova.py
├── technova_policy.txt
├── README.md
├── .gitignore
└── .venv/                 # Local virtual environment; do not commit
```

## Requirements

- Python 3.10 or later recommended
- An NVIDIA API key with access to a supported chat model
- Internet access for NVIDIA API requests and the first download of the embedding model

## Installation and Setup

### 1. Create and activate a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -U langchain langchain-community langchain-openai langchain-text-splitters langchain-huggingface sentence-transformers faiss-cpu
```

### 3. Configure the NVIDIA API key

```bash
export NVIDIA_API_KEY="your-nvidia-api-key"
```

Replace the placeholder with your actual NVIDIA API key. Never hardcode the key in the Python file or commit it to GitHub.

### 4. Add the policy document

Place `technova_policy.txt` in the same directory as `technova.py`. The script reads this local file and does not download the Google Doc at runtime.

### 5. Run the application

```bash
python technova.py
```

On the first run, Hugging Face may download the embedding model `sentence-transformers/all-MiniLM-L6-v2`. The application then creates a FAISS vector store and answers the three test questions.

The NVIDIA chat model is configured in `technova.py`. Make sure the model name is currently available to your NVIDIA API account.

## Sample Output

The following output was produced by running the application:

```text
Question 1: How many paid annual leave days does a full-time employee receive per year?
Answer: A full-time employee receives 18 paid annual leave days per calendar year.

Question 2: An employee wants to work remotely on Wednesday and take leave on Friday. What do the company policies say about these two requests?
Answer: Remote work is allowed on Wednesdays and Fridays, and employees must inform their manager by email at least one working day in advance. Remote work is subject to manager approval. Annual leave must be requested at least 3 calendar days before the requested leave date, and approval depends on the manager's confirmation.

Question 3: What is the company's parental leave policy?
Answer: The provided document does not specify this policy.
```

## Test Questions and Results

1. **Direct retrieval:** The system correctly retrieves the annual leave policy: 18 paid days per calendar year.
2. **Combining information:** The system combines the remote-work and annual-leave rules, including advance notice and manager approval.
3. **Information not present in the document:** The system states that the document does not specify the parental leave policy rather than inventing an answer.

## Security

- Never commit API keys, access tokens, or other secrets.
- Keep `.venv/` out of version control.
- Only publish `technova_policy.txt` if you have permission to share the document publicly.

## Author

Abhishek Kumar
