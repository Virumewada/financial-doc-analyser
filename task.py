# task.py - FINAL WORKING VERSION
from crewai import Task
from agents import verifier

analyze_financial_document = Task(
    description=(
        "Analyze the following financial document content: '{document_content}'. "
        "First, the Verifier agent must confirm that this text appears to be from a financial document. "
        "Then, the other agents in the crew will sequentially analyze it for market trends, risks, and provide an investment recommendation."
    ),
    expected_output="A final, comprehensive report in Markdown format.",
    agent=verifier
)