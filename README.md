<!-- prettier-ignore -->
<div align="center">

# GitHub Repo RAG


[Features](#features) • [Demo](#demo) • [Getting Started](#getting-started) • [Usage](#usage) • [Architecture](#architecture) • [Configuration](#configuration)

</div>

## Overview

**GitHub Repo RAG** is an intelligent assistant that clones, indexes, and lets you chat with any public GitHub repository. It leverages a sophisticated multi-stage retrieval pipeline to find the most relevant code, documentation, and notebook content, then answers your questions with citations to specific files.

Whether you want to understand a project's architecture, find the implementation of a specific function, or debug an issue, this tool quickly surfaces the right context from the codebase.

## Features

- **One-Click Cloning** — Paste a GitHub URL and the repository is automatically cloned, pulled, and indexed.
- **Hybrid Search** — Combines dense vector search (ChromaDB + Sentence Transformers) with sparse BM25 retrieval for high-accuracy document matching.
- **Intelligent Retrieval Planning** — An LLM-based planner analyzes each question to determine the search strategy, query rewrites, and preferred document types.
- **Context Validation** — Validates whether retrieved context is sufficient. If not, it performs targeted follow-up searches automatically.
- **Document Re-ranking** — Reranks retrieved documents to maximize relevance before answering.
- **Repository Analysis** — Automatically builds a repository profile identifying key files, entry points, symbols, and architecture.
- **AST-Based Code Chunking** — Parses Python files into semantic chunks using the abstract syntax tree, preserving function and class boundaries.
- **Modern Web UI** — Clean, responsive interface for loading repos and chatting, built with vanilla JavaScript and FastAPI.
- **Multiple File Types** — Supports `.py`, `.js`, `.ts`, `.java`, `.md`, `.txt`, `.json`, `.ipynb`, `.yaml`, `.yml`, `.cpp`, and `.c` files.

## Demo

1. Enter any public GitHub repository URL into the web interface.
2. The app clones the repo, indexes all documents, and builds a QA chain in the background.
3. Ask questions like:
   - "What does this project do?"
   - "Where is the main entry point?"
   - "How is the data model structured?"
   - "Show me the implementation of `build_qa_chain`"

## Getting Started

### Prerequisites

- Python 3.10+
- [Git](https://git-scm.com/downloads)
- A [Groq](https://groq.com/) API key (free tier available)

### Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/sushma-2003/Githubrep_clone_with_Agent_localhost.git
   cd Githubrep_clone_with_Agent_localhost
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure your environment:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set your Groq API key:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   > [!TIP]
   > You can get a free Groq API key at [console.groq.com](https://console.groq.com/keys).

### Running the Application

Start the FastAPI server:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:8000`.

Open your browser, paste a GitHub repository URL, and start exploring!

## Usage

### Web Interface

1. Navigate to `http://127.0.0.1:8000`
2. Enter a public GitHub repository URL (e.g., `https://github.com/torvalds/linux`)
3. Wait for the cloning, indexing, and QA chain to build (status is shown with a progress indicator)
4. Once ready, ask questions about the codebase in natural language

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | Serves the web interface |
| `/api/load` | `POST` | Start loading a repository (clone + index) |
| `/api/status/{session_id}` | `GET` | Poll the current status of a loading job |
| `/api/ask` | `POST` | Ask a question about the loaded repository |
| `/api/health` | `GET` | Health check |

### Example API Request

```bash
curl -X POST http://127.0.0.1:8000/api/load \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/microsoft/DeepSpeed"}'
```

```bash
curl -X POST http://127.0.0.1:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<your-session-id>", "question": "What is the main purpose of this project?"}'
```

## Architecture

```
User Query
    |
    v
Retrieval Planner (LLM)  <-- Determines question type & search strategy
    |
    v
Hybrid Retriever  <-- Dense (ChromaDB + Sentence Transformers) + Sparse (BM25)
    |
    v
Document Re-ranking  <-- Reranks documents for relevance
    |
    v
Context Validator  <-- Checks if context is sufficient; performs follow-up if needed
    |
    v
QA Chain (Groq LLM)  <-- Generates answer with source citations
```

### Component Overview

| Component | Purpose |
|-------------|---------|
| `app.py` | FastAPI web application and API endpoints |
| `clone_repo.py` | Clones or pulls GitHub repositories |
| `document_loader.py` | Loads and processes files from cloned repos |
| `chunking.py` | AST-based and semantic chunking for code files |
| `ingest.py` | Creates and persists the ChromaDB vector store |
| `retrievers.py` | Hybrid dense + sparse document retriever |
| `reranker.py` | Re-ranks retrieved documents by relevance |
| `agent_planner.py` | LLM-based retrieval planning and query generation |
| `context_validator.py` | Validates context sufficiency, triggers follow-up |
| `repo_analyzer.py` | Analyzes repository structure and builds a profile |
| `qa_chain.py` | Orchestrates the full QA pipeline |
| `query_rewriter.py` | Rewrites and expands search queries |
| `prompts.py` | System prompt templates for the LLM |

### Key Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)** — Modern, fast web framework for the API and static file serving
- **[LangChain](https://www.langchain.com/)** — LLM orchestration and chaining
- **[ChromaDB](https://www.trychroma.com/)** — Vector database for dense semantic search
- **[Sentence Transformers](https://www.sbert.net/)** — Embeddings (`all-MiniLM-L6-v2`)
- **[Groq API](https://groq.com/)** — Fast inference for the `openai/gpt-oss-120b` LLM
- **[NLTK](https://www.nltk.org/)** — Natural language tokenization for semantic chunking
- **[GitPython](https://gitpython.readthedocs.io/)** — Programmatic Git operations

## Configuration

The application is configured via the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | *(required)* |
| `DEBUG_RETRIEVAL` | Set to `1` to print retrieval debug info | `0` |

### Customizing the Embeddings Model

To use a different embedding model, edit `ingest.py`:

```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

Replace with any model compatible with [HuggingFaceEmbeddings](https://python.langchain.com/docs/integrations/text_embedding/huggingface/) from `langchain-huggingface`.

## Supported File Types

The following file extensions are indexed by default:

`.py` `.js` `.ts` `.java` `.cpp` `.c` `.md` `.txt` `.json` `.ipynb` `.yaml` `.yml`

To add more, update the `VALID_EXTENSIONS` tuple in `document_loader.py`.

## Troubleshooting

**ChromaDB import errors**
> Ensure OpenTelemetry dependencies are aligned. The `requirements.txt` pins compatible versions of `opentelemetry-api`, `opentelemetry-sdk`, and related packages.

**Repository not found / cloning fails**
> Verify the repository is public and the URL is correct. The app does not support private repositories without authentication.

**Slow indexing on large repositories**
> Indexing a very large repository (e.g., Linux kernel) can take time. The embedding step is CPU-bound. Consider using a GPU for `sentence-transformers` or selecting a smaller embedding model for faster indexing.

## Resources

- [Groq Console](https://console.groq.com/) — Get your API key and manage usage
- [LangChain Documentation](https://python.langchain.com/) — Learn about chains, retrievers, and agents
- [ChromaDB Documentation](https://docs.trychroma.com/) — Vector search and persistence
- [Sentence Transformers](https://www.sbert.net/) — Pre-trained sentence and text embeddings
