from transformers import pipeline

classifier = pipeline("text-classification", model="distilbert-base-uncased")

def prioritize_email(text):
    categories = ["Urgent", "Follow-up", "Low Priority"]
    prediction = classifier(text)
    return categories[min(int(prediction[0]["label"]), len(categories) - 1)]


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_email(text):
    summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
    return summary[0]["summary_text"]

import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_quick_reply(email_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Generate a professional reply for: {email_text}"}]
    )
    return response["choices"][0]["message"]["content"]


