import json
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("subscription_key")
api_base = os.getenv("endpoint")
api_version = os.getenv("api_version")
deployment_name = os.getenv("deployment")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_base
)

def format_prescription_summary(parsed_json):
    """
    Returns a readable, structured summary string from parsed JSON.
    Also creates an instruction-style summary (name + dose + freq).
    """
    lines = []
    instructions = []

    lines.append(f"👤 Patient: {parsed_json.get('patient_name', '')}")
    lines.append(f"👨‍⚕️ Doctor: {parsed_json.get('doctor_name', '')}")
    lines.append(f"🗓️ Date: {parsed_json.get('invoice_date', '')}")
    lines.append("")

    if "medicines" in parsed_json:
        lines.append("💊 Medicines:")
        for med in parsed_json["medicines"]:
            name = med.get("name", "")
            dosage = med.get("dosage", "")
            qty = med.get("quantity", "")
            freq = med.get("frequency", "")
            lines.append(f"- {name} ({dosage}), Qty: {qty}, Freq: {freq}")
            if name:
                instructions.append(f"1. Take {name} {dosage} {f'({freq})' if freq else ''}.")

    if parsed_json.get("notes"):
        lines.append("")
        lines.append(f"📝 Notes: {parsed_json['notes']}")

    return "\n".join(lines), "\n".join(instructions)

def translate_summary(text, target_language):
    """
    Usin GPT to translate the given text into the selected language.
    """
    prompt = f"""
Translate the following text into {target_language}:

{text}
    """

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

def generate_natural_summary(parsed_json):
    """
    Asks GPT to generate a natural 2–3 line patient-friendly summary.
    """
    prompt = f"""
You are a medical assistant. Based on the following prescription JSON data, generate a simple, 2–3 line bullet-point summary that a patient can easily understand. Use simple terms.

Respond with only the summary. Do not repeat the JSON or add explanations.

Prescription data:
```json
{json.dumps(parsed_json, indent=2)}
```
    """

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()