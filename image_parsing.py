import base64
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load env vars
load_dotenv()
api_key = os.getenv("subscription_key")
api_base = os.getenv("endpoint")
api_version = os.getenv("api_version")
deployment_name = os.getenv("deployment")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_base
)

def image_to_base64(image_bytes):
    """Convert image bytes to base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")

def extract_prescription(image_bytes):
    """Send image + prompt to GPT-4o and return structured JSON content."""
    base64_image = image_to_base64(image_bytes)

    prompt = f"""
You are an expert medical assistant helping users understand unstructured text extracted from scanned **Indian medical prescriptions** or **pharmacy bills**. These documents may be handwritten or printed, contain spelling mistakes, extra billing info, or irrelevant legal disclaimers.

Your job is to:
- **Correct obvious spelling errors** using your medical knowledge (e.g., “CIPCAL” is correct, not “ClPCAL”)
- **Ignore irrelevant information** like store disclaimers, GST, invoice codes, etc.
- **Extract only useful clinical or purchase details** like doctor name, medicines, dosages, quantities, etc.
- **Output the result in strict JSON**, using only the following keys:

```json
{{
  "patient_name": "",
  "doctor_name": "",
  "invoice_date": "",
  "medicines": [
    {{
      "name": "",
      "dosage": "",
      "quantity": "",
      "frequency": ""
    }}
  ],
  "notes": ""
}}

Do not include any extra keys or text outside this JSON.
If a value is not available, return it as an empty string ("").

 Here are some examples of the expected output format:

 {{
  "patient_name": "John Doe",
  "doctor_name": "Dr. Priya Mehta",
  "invoice_date": "2024-02-01",
  "medicines": [
    {{
      "name": "Amoxicillin",
      "dosage": "500mg",
      "quantity": "",
      "frequency": "Twice daily for 5 days"
    }},
    {{
      "name": "Dolo",
      "dosage": "650mg",
      "quantity": "",
      "frequency": "1 tablet after food"
    }}
  ],
  "notes": "Consult after 1 week."
}}
Now process the following raw text and respond with the corrected, structured JSON only:

"""

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
