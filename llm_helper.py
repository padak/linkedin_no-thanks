import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Ensure API key is set
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable not set. LLM features will fail.")
else:
    genai.configure(api_key=api_key)

SYSTEM_PROMPT = """
You are a helpful assistant for a busy tech professional. 
Your goal is to draft a polite but firm decline message to a sales pitch on LinkedIn.

Rules:
1. Detect the language of the incoming message (usually English or Czech).
2. Reply IN THE SAME LANGUAGE as the incoming message.
3. The core message is: "We use AI for this, so we don't need your services."
4. Tailor the message slightly to the specific offer (e.g., if they offer React devs, mention we use AI for coding; if they offer SEO, mention we use AI for content).
5. Keep it short and professional.
6. MANDATORY: You MUST end the message with this exact signature (translated to the target language):
   "This message was written by an Automatic robot I built myself."
   
   Czech translation: "Tuto zprávu napsal automatický robot, kterého jsem si sám postavil."
"""

def generate_response(incoming_message, sender_name):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')
        
        full_prompt = f"{SYSTEM_PROMPT}\n\nSender: {sender_name}\nMessage:\n{incoming_message}"
        
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        return None
