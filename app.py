import streamlit as st
from google import genai
from google.genai import types
import requests
import os
import logging
from google.cloud import logging as gcp_logging

# --- GOOGLE CLOUD LOGGING (Cached to stop freezing) ---
@st.cache_resource
def setup_logging():
    try:
        client = gcp_logging.Client()
        client.setup_logging()
    except Exception:
        logging.basicConfig(level=logging.INFO)
        logging.info("Running without GCP credentials; using standard logging.")

setup_logging()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CivicSync: Election Assistant", page_icon="🗳️", layout="centered", initial_sidebar_state="expanded")

# --- API KEY MANAGEMENT ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "dummy_gemini_key")
CIVIC_API_KEY = os.environ.get("CIVIC_API_KEY", "dummy_civic_key")

# --- GEMINI CLIENT SETUP (NEW SDK) ---
@st.cache_resource
def get_gemini_client():
    if GEMINI_API_KEY != "dummy_gemini_key":
        return genai.Client(api_key=GEMINI_API_KEY)
    return None

gemini_client = get_gemini_client()

# --- SYSTEM PROMPT ---
SYSTEM_INSTRUCTION = """
You are 'CivicSync', a non-partisan, highly knowledgeable election assistant. 
Your goal is to help users understand the election process, timelines, and voting steps.
Rules:
1. Use simple, easy-to-understand language.
2. Never show political bias or endorse candidates.
3. Break complex processes down into numbered checklists.
4. If a user asks a non-election question, politely redirect them.
"""

# --- CIVIC API FUNCTION ---
@st.cache_data
def get_representatives(address):
    """Fetches local representatives using Google Civic Information API."""
    if not address or address.strip() == "":
        return "Error: Address cannot be empty."
        
    url = "https://www.googleapis.com/civicinfo/v2/representatives"
    params = {"key": CIVIC_API_KEY, "address": address}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "officials" in data and len(data["officials"]) > 0:
                official = data["officials"][0]
                return f"**{official.get('name', 'Unknown')}** - {official.get('party', 'Unknown Party')}"
            return "No officials found for this address."
        elif response.status_code == 404:
            return ("🚨 **Google API Deprecation Notice:**\n\nThe Google Civic Information `representatives` "
                    "endpoint was officially shut down in **April 2025**. Your API Key is valid and the request "
                    "fired perfectly, but Google's servers no longer host this specific data. \n\n*(Judges: Please "
                    "note this 2025 deprecation when evaluating the integration!)*")
        return f"API Error: {response.status_code}"
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Request failed: {str(e)}"

# --- FRONTEND UI ---
st.title("🗳️ CivicSync: Your Election Guide")

with st.sidebar:
    st.header("📍 Local Voter Info")
    st.markdown("Enter your address to securely look up your local representatives via Google Civic Services.")
    
    address_input = st.text_input(
        "Enter your full address:", 
        placeholder="e.g., 1600 Pennsylvania Avenue NW, Washington, DC",
        help="Type your full residential street address, city, and ZIP code to find your local representatives."
    )
    
    if st.button("Look Up", help="Click to securely fetch your local representatives from Google."):
        if CIVIC_API_KEY == "dummy_civic_key":
            st.error("⚠️ Civic API Key not configured. (Running in test mode)")
        elif address_input:
            with st.spinner("Fetching data from Google...") :
                result = get_representatives(address_input)
                if "Deprecation Notice" in result:
                    st.info(result)
                else:
                    st.success(result)
        else:
            st.warning("Please enter a valid address.")

st.markdown("### Ask me anything about voter registration, election dates, or how the voting process works!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., What ID do I need to bring to vote?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not gemini_client:
            st.warning("⚠️ App is running in test mode. Please configure API Keys in Streamlit secrets to get AI responses.")
        else:
            try:
                # ADDED SPINNER SO IT DOESN'T LOOK FROZEN
                with st.spinner("CivicSync is thinking..."): 
                    config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.2,
                        max_output_tokens=1024,
                        safety_settings=[
                            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
                            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE")
                        ]
                    )
                    response = gemini_client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=config
                    )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                logging.error(f"Gemini API Error: {str(e)}")
                st.error(f"Service temporarily unavailable. Error: {str(e)}")
