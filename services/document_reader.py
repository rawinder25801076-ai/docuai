
import fitz
from docx import Document
from io import BytesIO

def extract_text(file):
    name = file.name.lower()
    content = file.getvalue()

    if name.endswith(".pdf"):
        pdf = fitz.open(stream=content, filetype="pdf")
        pages = []

        for i, page in enumerate(pdf):
            pages.append(
                f"Page {i + 1}\n{page.get_text()}"
            )

        return "\n\n".join(pages)

    elif name.endswith(".docx"):
        doc = Document(BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)

    elif name.endswith(".txt"):
        return content.decode("utf-8", errors="replace")

    return "Unsupported file format."
