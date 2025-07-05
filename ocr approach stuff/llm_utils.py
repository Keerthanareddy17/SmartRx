import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def clean_and_structure_text(raw_text):
    """
    Sends raw OCR text to Groq LLaMA-3.3 and returns structured prescription JSON.
    """
    prompt = f"""
You are a skilled AI assistant that interprets messy and unstructured OCR text extracted from Indian medical prescriptions or invoices. These documents may contain poor handwriting, formatting issues, or mixed content like GST info, disclaimers, etc.

Your job is to intelligently clean, interpret, and extract only medically relevant and useful details in structured JSON format. Prioritize extracting **medicine-related information**.

Respond ONLY with a JSON object. Do NOT include explanations or summaries.

Focus on understanding both prescriptions and receipts. Use your medical knowledge to fix OCR spelling issues
---

 Your tasks:
1. **Extract and structure these fields** when available:
    - `patient_name`: Name of the patient.
    - `doctor_name`: Name of the doctor (look for "Dr.", "Doctor", etc.).
    - `invoice_date`: Date of issue (e.g., near “Inv Date”, “Date”, etc.).
    - `pharmacy_name`: Store or hospital name (top/bottom of the receipt).
    - `total_amount`: Final billed amount (may appear as “Net Amt”, “Total”).
    - `medicines`: List of medicines with fields:
        - `name`
        - `dosage` (e.g., 500mg, 10ml)
        - `quantity` (e.g., No. of units, tablets, bottles)

2. **Be robust to OCR noise**. Fix common issues like:
    - "ClPCAL" → "CIPCAL"
    - "Syr BenadyI" → "Syr. Benadryl"
    - Date formats with slashes, dashes, or missing digits

3. **If a field is missing**, omit it entirely — don't guess or fill with placeholders.

---

Here is the raw OCR-extracted text:
\"\"\"{raw_text}\"\"\"
"""


    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    return chat_completion.choices[0].message.content.strip()