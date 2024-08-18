from crewai import Task
from agents import blood_test_analyst, article_researcher, health_advisor

# Define tasks
analyze_blood_test_task = Task(
    description='''
    You will be analyzing the following blood test report:
    "{text}"

    Instructions:
    1. Review each test result in the report.
    2. Identify the test name, the value, and the normal range.
    3. Compare the test value to the normal range:
        - If the value is within the normal range, note that it is normal.
        - If the value is outside the normal range, highlight it and explain the potential implications.
    4. Provide a comprehensive summary including:
        - An overview of all test results.
        - A detailed analysis of any abnormal values.
        - Potential implications of the abnormal results.
        - Suggestions for further investigation if needed.
    ''',
    expected_output='A comprehensive summary of the blood test results, highlighting abnormal values with explanations and potential implications.',
    agent=blood_test_analyst,
)

find_articles_task = Task(
    description='''
    Following the analysis of the blood test report, perform the following tasks:
    1. Identify key health concerns or issues highlighted by the abnormal values in the blood test report.
    2. Search the web for 3-5 recent, high-quality medical articles that are directly related to each identified health concern.
    3. For each selected article, provide:
        - The full title and author(s) of the article.
        - A concise summary of the main findings or recommendations.
        - A clear explanation of how the article's findings relate to the blood test results.
    ''',
    expected_output='A list of 3-5 carefully selected medical articles with summaries and relevance to the blood test results.',
    agent=article_researcher,
    context=[analyze_blood_test_task]
)

provide_recommendations_task = Task(
    description='''
    Based on the detailed analysis of the blood test report and the relevant articles, provide comprehensive health recommendations:
    1. Summarize the key findings from the blood test report and articles.
    2. Identify the main health concerns highlighted by the test results and articles.
    3. Recommend any additional tests or follow-ups that may be necessary for further evaluation.
    4. Offer actionable lifestyle advice aimed at improving overall health, considering the specific findings of the blood test.
    5. Include links to the referenced articles or additional trusted resources for further reading.
    ''',
    expected_output='A set of prioritized health recommendations, including a summary of findings, suggestions, and lifestyle advice.',
    agent=health_advisor,
    context=[analyze_blood_test_task, find_articles_task]
)
