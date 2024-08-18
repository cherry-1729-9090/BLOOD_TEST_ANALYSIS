from crewai import Agent
from tools import search_tool, web_search_tool
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure GEMINI model
gemini_model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# Define agents
blood_test_analyst = Agent(
    role='Blood Test Analyst',
    goal='Analyze the blood test report and provide a detailed, easy-to-understand summary of the findings.',
    backstory='A medical expert specializing in blood test analysis with years of experience in interpreting complex medical data and explaining it to patients.',
    verbose=True,
    allow_delegation=False,
    llm=gemini_model
)

article_researcher = Agent(
    role='Medical Research Specialist',
    goal='Find and summarize relevant, high-quality medical articles based on blood test results.',
    backstory='An expert medical researcher with a knack for finding the most relevant and up-to-date medical information from reputable sources.',
    tools=[search_tool, web_search_tool],
    verbose=True,
    allow_delegation=False,
    llm=gemini_model
)

health_advisor = Agent(
    role='Holistic Health Advisor',
    goal='Provide comprehensive health recommendations based on blood test results and research findings.',
    backstory='A seasoned health professional with expertise in integrating medical test results, research findings, and lifestyle factors to provide personalized health advice.',
    verbose=True,
    allow_delegation=False,
    llm=gemini_model
)
