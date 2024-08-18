import os
import json
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import Agent
from tools import search_tool, web_search_tool
from langchain_google_genai import ChatGoogleGenerativeAI
from PyPDF2 import PdfReader
from tasks import analyze_blood_test_task, find_articles_task, provide_recommendations_task

# Load environment variables
load_dotenv()

# Load the trained agent configurations
with open('trained_agents_config.json', 'r') as f:
    trained_configs = json.load(f)

# Configure the GEMINI model
gemini_model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# Function to get agent configuration from the list
def get_agent_config(agent_role, configs):
    for config in configs:
        if config['role'] == agent_role:
            return config
    return None

# Initialize the agents with the trained configurations
blood_test_analyst_config = get_agent_config('Blood Test Analyst', trained_configs)
article_researcher_config = get_agent_config('Medical Research Specialist', trained_configs)
health_advisor_config = get_agent_config('Holistic Health Advisor', trained_configs)

blood_test_analyst = Agent(
    role=blood_test_analyst_config['role'],
    goal=blood_test_analyst_config['goal'],
    backstory=blood_test_analyst_config['backstory'],
    verbose=True,
    allow_delegation=False,
    llm=gemini_model,
)

article_researcher = Agent(
    role=article_researcher_config['role'],
    goal=article_researcher_config['goal'],
    backstory=article_researcher_config['backstory'],
    tools=[search_tool, web_search_tool],
    verbose=True,
    allow_delegation=False,
    llm=gemini_model,
)

health_advisor = Agent(
    role=health_advisor_config['role'],
    goal=health_advisor_config['goal'],
    backstory=health_advisor_config['backstory'],
    verbose=True,
    allow_delegation=False,
    llm=gemini_model,
)

# Define the main function for the Streamlit app
def main():
    st.set_page_config(page_title="Medical Report Analysis", layout="wide")
    st.title("🩺 Medical Report Analysis")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)

        if st.button("Analyze Report"):
            st.write("Analyzing the report... This may take a few minutes.")

            # Create a Crew and execute tasks using the trained agents
            crew = Crew(
                agents=[blood_test_analyst, article_researcher, health_advisor],
                tasks=[analyze_blood_test_task, find_articles_task, provide_recommendations_task],
                verbose=True
            )

            # Kick off the crew process with the extracted text
            with st.spinner("Processing..."):
                try:
                    result = crew.kickoff(inputs={"text": text})

                    if isinstance(result, dict):
                        result_str = format_analysis(result)
                        st.markdown(result_str, unsafe_allow_html=True)
                    else:
                        st.markdown(result, unsafe_allow_html=True)  # Directly render the markdown

                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")
    return text

def format_analysis(result):
    output = f"""
    **Comprehensive Health Recommendations**

    **Summary of Findings:**

    * {' '.join(result.get('summary', []))}

    **Main Health Concerns:**

    * {' '.join(result.get('concerns', []))}

    **Additional Tests or Follow-Ups:**

    * {' '.join(result.get('follow_ups', []))}

    **Actionable Lifestyle Advice:**

    {format_lifestyle_advice(result.get('lifestyle', []))}

    **References:**

    {format_references(result.get('references', []))}
    """
    return output

def format_lifestyle_advice(advice_list):
    formatted_advice = ""
    for advice in advice_list:
        formatted_advice += f"* {advice}\n"
    return formatted_advice

def format_references(ref_list):
    formatted_references = ""
    for ref in ref_list:
        formatted_references += f"* [{ref}]({ref})\n"
    return formatted_references

if __name__ == "__main__":
    main()
