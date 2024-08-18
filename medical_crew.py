from crewai import Agent
from tools import search_tool, web_search_tool
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure GEMINI model with appropriate settings
gemini_model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

class BloodTestAnalyst(Agent):
    def __init__(self):
        super().__init__(
            role='Blood Test Analyst',
            goal="Analyze the blood test report, identify key abnormalities...",
            backstory="A seasoned hematologist with over a decade of experience...",
            verbose=True,
            allow_delegation=False,
            llm=gemini_model
        )

    def analyze_report(self, input_data):
        # Implement the analysis logic
        return "analysis result"

class MedicalResearchSpecialist(Agent):
    def __init__(self):
        super().__init__(
            role='Medical Research Specialist',
            goal="Identify and summarize relevant medical articles...",
            backstory="An accomplished medical researcher...",
            tools=[search_tool, web_search_tool],
            verbose=True,
            allow_delegation=False,
            llm=gemini_model
        )

    def conduct_research(self, input_data):
        # Implement the research logic
        return "research result"

class HolisticHealthAdvisor(Agent):
    def __init__(self):
        super().__init__(
            role='Holistic Health Advisor',
            goal="Provide personalized health recommendations...",
            backstory="A holistic health practitioner with a deep understanding...",
            verbose=True,
            allow_delegation=False,
            llm=gemini_model
        )

    def provide_recommendations(self, input_data):
        # Implement the recommendation logic
        return "recommendations result"

class MedicalCrew:
    def __init__(self):
        self.agents = [
            BloodTestAnalyst(),
            MedicalResearchSpecialist(),
            HolisticHealthAdvisor()
        ]
    
    def crew(self):
        return self.agents
