# main.py - FINAL WORKING VERSION
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import uvicorn
from dotenv import load_dotenv
import pypdf # Library to read PDFs

load_dotenv()

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document

app = FastAPI(title="Financial Document Analyzer")

async def run_crew(query: str, document_content: str):
    # Update the task with the actual document content
    analyze_financial_document.description = analyze_financial_document.description.format(document_content=document_content)

    financial_crew = Crew(
        agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
        tasks=[analyze_financial_document],
        process=Process.sequential,
        verbose=True
    )
    result = financial_crew.kickoff(inputs={'query': query})
    return result

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze the provided financial text for investment insights")
):
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    file_path = f"data/financial_document_{file_id}{file_extension}"

    try:
        os.makedirs("data", exist_ok=True)
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # --- NEW LOGIC TO READ PDF AND PASS CONTENT ---
        document_text = ""
        if file_extension.lower() == ".pdf":
            pdf_reader = pypdf.PdfReader(file_path)
            for page in pdf_reader.pages:
                document_text += page.extract_text()
        else:
            # For non-PDF files, assume it's a text file
            document_text = content.decode('utf-8')

        if not document_text:
            raise HTTPException(status_code=400, detail="Could not extract text from the document.")

        response = await run_crew(query=query.strip(), document_content=document_text)
        # --- END OF NEW LOGIC ---

        return { "status": "success", "analysis": str(response) }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)