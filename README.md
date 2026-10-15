TechNova Policy RAG Using LangChain
A Retrieval-Augmented Generation (RAG) application that answers employee questions using the TechNova Solutions policy document.
Features
- Loads technova_policy.txt from the same folder as the Python script.
- Splits the document into overlapping text chunks.
- Generates embeddings locally with Hugging Face.
- Stores and searches embeddings using FAISS.
- Retrieves the three most relevant chunks for each question.
- Uses an NVIDIA-hosted chat model to generate answers from the retrieved context.
- Instructs the model to state when the document does not contain the requested policy.
Tech Stack
- Python
- LangChain
- Hugging Face Sentence Transformers
- FAISS
- NVIDIA API Catalog / NVIDIA-hosted model
Project Structure
technova-policy-rag-langchain/
├── technova.py
├── technova_policy.txt
├── README.md
├── .gitignore
└── .venv/                 # Local virtual environment; do not commit
Requirements
- Python 3.10 or later recommended
- An NVIDIA API key with access to a supported chat model
- Internet access for NVIDIA API requests and the first download of the local embedding model
Setup
1. Create and activate a virtual environment
Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate
2. Install dependencies
python -m pip install --upgrade pip
pip install -U langchain langchain-community langchain-openai langchain-text-splitters langchain-huggingface sentence-transformers faiss-cpu
3. Set your NVIDIA API key
Linux/macOS:
export NVIDIA_API_KEY="your-nvidia-api-key"
Do not put your API key in the source code or commit it to GitHub.
4. Add the policy document
Place technova_policy.txt in the same directory as technova.py. The script reads the local file; it does not download the Google Doc at runtime.
5. Run the application
python technova.py
On the first run, Hugging Face may download the embedding model sentence-transformers/all-MiniLM-L6-v2. The script then builds the FAISS index and answers the three test questions.
The configured NVIDIA model is meta/llama-3.1-8b-instruct. If that model is not available to your account, select a currently supported chat model in the NVIDIA API Catalog and update the model value in technova.py.
Test Questions
1. How many paid annual leave days does a full-time employee receive per year?
2. An employee wants to work remotely on Wednesday and take leave on Friday. What do the company policies say about these two requests?
3. What is the company's parental leave policy?
Expected Behavior
- Question 1: Identify the 18 paid annual leave days per calendar year and mention the request deadline and manager approval requirement.
- Question 2: Explain the remote-work notice and approval requirements and the annual-leave notice and approval requirements.
- Question 3: State that the provided document does not specify the parental leave policy.
These are expected behaviors, not guaranteed verbatim outputs. Actual wording depends on the model response.
Security
- Never commit API keys, access tokens, or .env files.
- Keep .venv/ out of version control.
- Only publish technova_policy.txt if you have permission to share the document publicly.
