# src/claim_agent/claim_agent.py

from crewai import Agent
from tools.nlp import spacy_claim_analyzer_tool
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
os.environ['GOOGLE_API_KEY']= os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model= "gemini-2.5-flash",
    temperature=0.1
    )

claim_agent = Agent(
    role="Claim Evaluator and NER Extractor",
    goal=(
        "Analyze user-provided claims to extract named entities and assess "
        "how sensationalized they are using linguistic patterns."
    ),
    backstory=(
        "You are a data journalist AI who verifies and evaluates claims. "
        "You identify factual elements (entities) and detect sensationalism "
        "using natural language analysis."
    ),
    tools=[spacy_claim_analyzer_tool],
    verbose=False,
    memory=False,
    allow_delegation=False,
    llm=llm
)
