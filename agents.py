# agents.py - Final Version without FileReadTool
import os
from dotenv import load_dotenv
from crewai import Agent
from tools import search_tool # We only import search_tool now
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", verbose=True, temperature=0.5, google_api_key=os.getenv("GOOGLE_API_KEY"))

financial_analyst = Agent(role="Senior Financial Analyst", goal="Provide insightful, data-driven investment advice.", verbose=True, memory=True, backstory="A seasoned analyst.", tools=[search_tool], allow_delegation=True, llm=llm)
verifier = Agent(role="Document Verifier", goal="Verify the provided text is a financial document.", verbose=True, memory=True, backstory="A detail-oriented verifier.", tools=[], allow_delegation=False, llm=llm) # No tools needed
investment_advisor = Agent(role="Investment Advisor", goal="Recommend investment strategies.", verbose=True, backstory="A prudent advisor.", tools=[search_tool], allow_delegation=False, llm=llm)
risk_assessor = Agent(role="Risk Assessor", goal="Assess investment risks.", verbose=True, backstory="A cautious risk analyst.", tools=[search_tool], allow_delegation=True, llm=llm)