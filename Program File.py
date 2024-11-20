import sqlite3
import openai
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def analyze_sentiment_and_aspects(text):
    response = openai.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Analyze the sentiment of this comment: '{text}' and extract key positive and negative aspects from the comment. Respond with 'Sentiment: [Positive/Negative/Neutral]', 'Positive Aspects: [list of positive aspects]', and 'Negative Aspects: [list of negative aspects]'."}
        ]
    )
    return response.choices[0].message.content.strip()

# Connect to the original SQLite database
conn = sqlite3.connect('feedback.db')
cursor = conn.cursor()
cursor.execute("SELECT comment FROM feedback")
comments = cursor.fetchall()

# Create a new SQLite database to store the results
new_conn = sqlite3.connect('feedback_analysis.db')
new_cursor = new_conn.cursor()
new_cursor.execute('''CREATE TABLE analysis (
                      id INTEGER PRIMARY KEY,
                      comment TEXT,
                      sentiment TEXT,
                      positive_aspects TEXT,
                      negative_aspects TEXT
                      )''')

# Perform sentiment analysis and insert results
for comment in comments:
    comment_text = comment[0]
    print(f"Processing comment: {comment_text}")  # Debug print
    analysis = analyze_sentiment_and_aspects(comment_text)
    print(f"Analysis result: {analysis}")  # Debug print

    # Parsing the analysis result
    sentiment = analysis.split("Sentiment:")[1].split("Positive Aspects:")[0].strip()
    positive_aspects = analysis.split("Positive Aspects:")[1].split("Negative Aspects:")[0].strip()
    negative_aspects = analysis.split("Negative Aspects:")[1].strip()

    print(f"Sentiment: {sentiment}")  # Debug print
    print(f"Positive Aspects: {positive_aspects}")  # Debug print
    print(f"Negative Aspects: {negative_aspects}")  # Debug print

    # Insert the analysis result into the new database
    new_cursor.execute("INSERT INTO analysis (comment, sentiment, positive_aspects, negative_aspects) VALUES (?, ?, ?, ?)", 
                       (comment_text, sentiment, positive_aspects, negative_aspects))

# Commit the changes and close the new database connection
new_conn.commit()
new_conn.close()

# Close the original database connection
conn.close()