
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY is missing from your .env file")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=API_KEY,
    temperature=0.3,
    max_tokens=2048
)


def ask_ai(prompt):
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as error:
        return f"AI Error: {error}"


def summarize_document(document_text):
    document_text = document_text[:20000]

    prompt = f"""
You are DocuMind AI, an intelligent document assistant.

Analyse the document and provide:

1. Document overview
2. Important topics
3. Key points
4. Important definitions
5. Conclusion

Use simple, understandable English.
Do not invent information.

DOCUMENT:
{document_text}
"""
    return ask_ai(prompt)


def answer_document(document_text, question):
    document_text = document_text[:20000]

    prompt = f"""
You are DocuMind AI. Answer the user's question using the
provided document.

Rules:
- Use information from the document.
- Explain in simple English.
- Do not invent facts.
- If the answer is missing, say:
  "This information was not found in the provided document."

DOCUMENT:
{document_text}

QUESTION:
{question}
"""
    return ask_ai(prompt)


def generate_study_notes(document_text):
    document_text = document_text[:20000]

    prompt = f"""
You are DocuMind AI, an expert study notes assistant.

Create clear, well-organized study notes using ONLY the
information available in the provided document.

Use this structure:

# Study Notes

## 1. Chapter / Document Overview
Explain the main subject briefly.

## 2. Important Topics
List the major topics and explain each briefly.

## 3. Detailed Study Notes
Organize the important information under meaningful headings.
Use bullet points and simple explanations.

## 4. Important Definitions
List important terms and their definitions.

## 5. Important Formulas and Facts
Include formulas, equations, dates, figures or facts only
if they appear in the document.
If none are found, say so.

## 6. Quick Revision Points
Create a concise revision checklist.

## 7. Important Practice Questions
Create up to 10 questions based on the document.
Include a mixture of short-answer and descriptive questions.
Do not invent topics outside the document.

IMPORTANT RULES:
- Preserve the meaning of the original document.
- Do not add unsupported information.
- Use simple, student-friendly English.
- Make the notes useful for exam preparation.
- Use Markdown headings and bullet points.

DOCUMENT:
{document_text}
"""

    return ask_ai(prompt)
