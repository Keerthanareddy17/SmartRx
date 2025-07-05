# 💊 SmartRx – AI Prescription Reader

SmartRx is a lightweight Streamlit-based AI tool that helps users **extract, understand, and translate information from medical prescriptions**. 

Whether it’s handwritten or printed, we try to pull out key medical details and summarize it in a way that’s easy to read and share.......and also translate it to your favourite language :)  

Perfect for patients, caregivers, or pharmacists who want clarity on what’s written on a prescription.

---

## ✨ What does it exactly do?!

SmartRx allows you to:

- 📸 Upload an image of a medical prescription or pharmacy bill  
- 🤖 Automatically extract important information like:
  - Patient name  
  - Doctor’s name  
  - Date  
  - List of medicines with dosage, quantity, and frequency.....
- 🧠 Summarize the prescription into 2-3 simple bullet points  
- 🌍 Translate the summary into your local language  
- 📤 Download the extracted or translated text  
- 📲 Share it via WhatsApp to your desired number *(automation-ready)*

All of this happens right inside a clean, user-friendly web UI.

---

## 🛠️ Workflow.....

Here’s the step-by-step idea:

1. I used **Azure GPT-4o (API)** to extract structured data from a base64 image of the prescription.
2. The model is guided with a well-engineered prompt to return clean JSON.
3. This output is parsed, cleaned, and displayed beautifully in Streamlit.
4. We then generate a summary based on the extracted medicines.
5. The summary can be translated to several Indian and global languages using GPT itself.
6. The translated message can be sent via WhatsApp automation using `pywhatkit`.

<img width="622" alt="Screenshot 2025-07-05 at 22 02 29" src="https://github.com/user-attachments/assets/a516da6e-a77c-4986-89c2-a5f3c59522c4" />


---

## 🧰 Tech Stack

- **Frontend & UI**: [Streamlit](https://streamlit.io/)  
- **AI Processing**: `OpenAI GPT-4o` 
- **Environment Management**: `dotenv`  
- **Translation**: GPT prompt-based  
- **WhatsApp Automation )**: [`pywhatkit`](https://pypi.org/project/pywhatkit/)  
- **Data Handling**: `pandas`, `json`, `re`

---
## 📸 Snapshots of SmartRx

![output1](https://github.com/user-attachments/assets/10ccc19f-c908-4129-a338-1b2295b4eacd)



![output2](https://github.com/user-attachments/assets/d8709dc2-add4-40d0-a464-bdbe72f36ed6)




This is just the starting point. Here’s what we (or you!) can build next:

- ✅ OCR fallback for extremely low-quality images
- 🔒 Secure storage/logging of processed data (with user consent)
- 📥 Support for PDF input (multi-page prescriptions)
- 🗂️ Create user accounts & history (save past prescriptions)
- 💬 Add voice summary support for elderly users

---

## 👋 Want to say hi or collaborate?

If you have ideas, questions, or want to build on this — feel free to connect!

🐙 Linkedin : [Katasani Keerthana Reddy](https://www.linkedin.com/in/keerthana-reddy-katasani-b07238268/)**  
📧 Email: katasanikeerthanareddy@gmail.com  
