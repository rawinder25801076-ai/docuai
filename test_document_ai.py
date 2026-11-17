
from services.ai_engine import summarize_document

sample_document = """
Artificial Intelligence is a branch of computer science.
It focuses on creating machines that can perform tasks
that normally require human intelligence.

Machine learning is a part of AI that allows computers
to learn patterns from data and improve their performance.
"""

result = summarize_document(sample_document)

print("\nDOCUMIND AI DOCUMENT SUMMARY:\n")
print(result)
