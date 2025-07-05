import streamlit as st
import json
from image_parsing import extract_prescription
import pandas as pd
import re
from translate import format_prescription_summary, translate_summary, generate_natural_summary
from whatsapp_utils import send_whatsapp_message

# Page config
st.set_page_config(page_title="SmartRx", page_icon="💊")

st.markdown("""
    <style>
    .main {
        font-family: 'Segoe UI', sans-serif;
    }

    h1, h2, h3 {
        color: #66ccff;
    }

    .info-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #1c1c1c;
        border: 1px solid #333;
        margin-bottom: 1rem;
    }

    .label {
        color: #cccccc;
        font-weight: bold;
    }

    .value {
        color: #ffffff;
    }

    table {
        background-color: #2d2d2d;
        color: white;
    }

    th {
        background-color: #444;
        color: #ddd;
    }

    td {
        background-color: #222;
        color: #eee;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💊 SmartRx - AI Prescription Reader")

# Utility function to clean GPT output
def clean_json_text(raw_output):
    """
    Removes markdown code block markers and invisible characters for safe JSON parsing.
    """
    cleaned = re.sub(r"^```(?:json)?", "", raw_output.strip(), flags=re.IGNORECASE | re.MULTILINE)
    cleaned = cleaned.replace("```", "").strip()
    cleaned = cleaned.encode("utf-8", "ignore").decode("utf-8")
    return cleaned

# File uploader
uploaded_file = st.file_uploader("📷 Upload a prescription image", type=["jpg", "jpeg", "png"])

parsed = None  

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Prescription", use_container_width=True)

    with st.spinner("Processing with GPT-4o..."):
        image_bytes = uploaded_file.read()
        try:
            output = extract_prescription(image_bytes)


            cleaned_output = clean_json_text(output)

            try:
                parsed = json.loads(cleaned_output)
                st.success("✅ Extracted Successfully!")

                # --- Styled Info ---
                st.subheader("📋 Extracted Info")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                        <div class="info-card">
                            <div class="label">👤 Patient Name:</div>
                            <div class="value">{parsed.get('patient_name', '')}</div>
                        </div>
                        <div class="info-card">
                            <div class="label">👨‍⚕️ Doctor Name:</div>
                            <div class="value">{parsed.get('doctor_name', '')}</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                        <div class="info-card">
                            <div class="label">🗓️ Date:</div>
                            <div class="value">{parsed.get('invoice_date', '')}</div>
                        </div>
                        <div class="info-card">
                            <div class="label">📝 Notes:</div>
                            <div class="value">{parsed.get('notes', '')}</div>
                        </div>
                    """, unsafe_allow_html=True)

                if "medicines" in parsed and isinstance(parsed["medicines"], list):
                    st.subheader(" Medicines")
                    for med in parsed["medicines"]:
                        if med.get("name"):
                            med["name"] = f"💊 {med['name']}"
                    st.table(pd.DataFrame(parsed["medicines"]))

                st.download_button(
                    label="⬇️ Download as JSON",
                    data=json.dumps(parsed, indent=2),
                    file_name="prescription.json",
                    mime="application/json",
                    type="primary"
                )

                st.download_button(
                    label="⬇️ Download as TXT",
                    data=cleaned_output,
                    file_name="prescription.txt",
                    mime="text/plain"
                )

            except json.JSONDecodeError:
                st.warning("⚠️ Could not parse output as JSON. Showing raw response only.")
                st.code(cleaned_output, language="text")

        except Exception as e:
            st.error("❌ Error while processing the image.")
            st.exception(e)

# Translation Section 
st.subheader("🌐 Translate ")
language_options = ["None", "Hindi", "Telugu", "Tamil", "Kannada", "Marathi", "Bengali", "Gujarati"]
target_language = st.selectbox("Choose target language for translation", language_options)

if target_language != "None" and parsed:
    summary, instructions = format_prescription_summary(parsed)
    natural_summary = generate_natural_summary(parsed)

    combined_text = summary + "\n\n" + instructions + "\n\n" + natural_summary

    with st.spinner(f"Translating to {target_language}..."):
        translated = translate_summary(combined_text, target_language)
        st.markdown("### 📄 Translated Summary")
        st.text(translated)

        st.download_button(
            label="⬇️ Download Translation",
            data=translated,
            file_name=f"prescription_{target_language.lower()}.txt",
            mime="text/plain"
        )

# WhatsApp Send
st.subheader("📲 Send to WhatsApp")

phone_input = st.text_input("Enter recipient's WhatsApp number (with country code, e.g. +91...)", max_chars=15)

if phone_input and translated:
    if st.button("📤 Send Message"):
        success = send_whatsapp_message(phone_input, translated)
        if success:
            st.success(f"✅ Message sent to {phone_input}")
        else:
            st.error("❌ Failed to send message. Make sure WhatsApp Web is logged in.")
