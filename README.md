# VWO - AI Internship Assignment: Financial Document Analyzer

This project is a financial document analysis system built with CrewAI. It provides a web API where a user can upload a financial document (like a PDF report) and submit a query. A crew of autonomous AI agents then collaborates to analyze the document, gather real-time market data, assess risks, and generate a comprehensive investment recommendation based on the findings.

---

## Bugs Found & Fixes Implemented

The original codebase was non-functional and contained numerous bugs across the environment, code, and logic. The debugging process involved a systematic, multi-level approach:

**1. Environment & Dependency Errors:**
* **Problem:** The initial `requirements.txt` file contained outdated and conflicting library versions (e.g., `pydantic` v1 vs v2, `onnxruntime`, `opentelemetry`, etc.), causing `ResolutionImpossible` errors. Some packages also failed to install due to a modern Python version (3.13) and missing C++ build tools on Windows.
* **Fix:**
    * Downgraded Python from 3.13 to a more stable version (3.11).
    * Installed the "Microsoft C++ Build Tools" to enable package compilation.
    * After many conflicts, I created a "golden" `requirements.txt` with specific, compatible versions of key libraries (`crewai==0.28.8`, etc.).
    * Finally, I created a fresh, clean virtual environment (`venv`) to resolve all leftover conflicts from previous installation attempts.

**2. Code-Level Bugs (Syntax & Logic):**
* **Problem:** The code had multiple `ImportError`s because the `crewai` and `crewai_tools` library structures had changed. It also had a `NameError` (`llm = llm`) and incorrect agent parameters (`tool` instead of `tools`, invalid `max_rpm`).
* **Fix:**
    * Corrected all import statements to match the modern library structure (e.g., `from crewai import Agent`).
    * Replaced the buggy `llm = llm` line with a proper initialization of the `ChatGoogleGenerativeAI` class.
    * Fixed all invalid agent parameters.
    * Replaced the buggy custom `FinancialDocumentTool` with the official, pre-built `FileReadTool` for better reliability.

**3. API Authentication & Configuration Errors:**
* **Problem:** The application was failing to find the Google API key (`DefaultCredentialsError`) and was incorrectly defaulting to the OpenAI API. Later, it failed because the model name (`gemini-pro`) was not found.
* **Fix:**
    * Implemented a robust method to load the API key from a `.env` file using `python-dotenv`.
    * Passed the key directly to the LLM instance to ensure it was found.
    * Corrected the model name to a valid, available model (`gemini-1.5-flash-latest`).

**4. AI Logic Bug:**
* **Problem:** Even after fixing all technical bugs, the AI agent was unable to find and read the file it was supposed to analyze.
* **Fix:** I re-architected the workflow. Instead of passing a file path to the agent, I modified `main.py` to first read the PDF content using the `pypdf` library and then pass the extracted text directly to the crew. This made the process much more reliable and separated file handling from AI analysis.

---

## Setup and Usage Instructions

1.  **Clone the repository:**
    ```bash
    git clone [your-github-repo-link]
    cd [your-project-folder]
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up API Key:**
    * Create a `.env` file in the root directory.
    * Add your Google AI API Key to it: `GOOGLE_API_KEY="your_api_key_here"`
5.  **Run the application:**
    ```bash
    python main.py
    ```

---

## API Documentation

The server runs on `http://127.0.0.1:8000`.

You can access the interactive API documentation (Swagger UI) by navigating to:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

From there, you can use the `/analyze` endpoint to upload a file and provide a query to test the application.
