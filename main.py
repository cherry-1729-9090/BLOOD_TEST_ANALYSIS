import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import blood_test_analyst, article_researcher, health_advisor
from tasks import analyze_blood_test_task, find_articles_task, provide_recommendations_task
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Define the main function for the Streamlit app
def main():
    st.set_page_config(page_title="Medical Report Analysis", layout="wide")
    st.title("🩺 Medical Report Analysis")

    st.markdown("""
    <style>
        .main-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #2E86C1;
        }
        .sub-title {
            font-size: 1.75em;
            font-weight: bold;
            margin-top: 20px;
            color: #2980B9;
        }
        .recommendation {
            margin-top: 20px;
            font-size: 1.25em;
            color: #1C2833;
        }
        .observation {
            font-size: 1.15em;
            margin-bottom: 15px;
            color: #34495E;
        }
    </style>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)

        if st.button("Analyze Report"):
            st.write("Analyzing the report... This may take a few minutes.")

            # Create a Crew and execute tasks
            crew = Crew(
                agents=[blood_test_analyst, article_researcher, health_advisor],
                tasks=[analyze_blood_test_task, find_articles_task, provide_recommendations_task],
                verbose=True
            )

            # Kick off the crew process with the extracted text
            with st.spinner("Processing..."):
                try:
                    result = crew.kickoff(inputs={"text": text})
                    st.write(result)  # Inspect the result object

                    if isinstance(result, str):
                        result_str = result
                    else:
                        result_str = format_analysis(result)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
                    return

            # Display results with enhanced styling
            st.markdown(result_str, unsafe_allow_html=True)

            # Save the results to a markdown file if needed
            # output_file = "results1.md"
            # with open(output_file, "w") as file:
            #     file.write(result_str)

            # st.success(f"Results have been written to {output_file}")

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
    # Check if result is a string or a dictionary
    if isinstance(result, str):
        return f"<h2 class='main-title'>Analysis Results</h2><p>{result}</p>"
    elif isinstance(result, dict):
        output = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2E86C1;">Analysis Results</h2>
            
            <h3 style="color: #2980B9;">Summary of Key Findings</h3>
            <p>{'. '.join(result.get('summary', [])).replace('- ', '')}</p>
            
            <h3 style="color: #2980B9;">Main Health Concerns</h3>
            <p>{'. '.join(result.get('concerns', [])).replace('- ', '')}</p>
            
            <h3 style="color: #2980B9;">Additional Tests or Follow-Ups</h3>
            <p>{'. '.join(result.get('follow_ups', [])).replace('- ', '')}</p>

            <h3 style="color: #2980B9;">Actionable Lifestyle Advice</h3>
            <p>{'. '.join(result.get('lifestyle', [])).replace('- ', '')}</p>

            <h3 style="color: #2980B9;">References</h3>
            <p>{' '.join([f'<a href="{ref}" target="_blank">{ref}</a>' for ref in result.get('references', [])])}</p>
        </div>
        """
        return output
    else:
        return "<p>An unexpected result format was returned. Please check the analysis.</p>"


if __name__ == "__main__":
    main()
