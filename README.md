# 🗳️ CivicSync: Election Assistant

## 📌 Chosen Vertical
**Election Process Education** - Providing voters with a non-partisan, easy-to-understand guide for registration, voting steps, and local representation.

## 🧠 Approach and Logic
Our logic relies on a dual-service architecture to maximize accuracy and usability:
1. **Google Gemini (1.5 Flash):** Acts as the conversational brain, guided by a strict System Prompt to ensure simple language, absolute political neutrality, and redirection of non-civic queries.
2. **Google Civic Information API:** Integrates live, localized data. Users input their address to securely fetch their real-world representatives, bridging the gap between AI advice and real-world application.

## ⚙️ How the Solution Works
- **User Interface:** Built with Streamlit for a clean, accessible chat interface.
- **Conversational Flow:** Users type questions about the election process. The app securely fetches the `GEMINI_API_KEY` from environment variables, queries the model, and displays the response.
- **Local Lookup:** Using the sidebar, the app securely passes the user's address and `CIVIC_API_KEY` to Google's Civic Info v2 endpoint, parses the JSON response, and surfaces the top local official.
- **Containerization:** The app is fully containerized using a `Dockerfile` exposing port 8080, making it enterprise-ready for Google Cloud Run.

## 🤔 Assumptions Made
- Users are querying about standard democratic election processes.
- The Google Civic API will return valid JSON for standard formatted addresses.
- Environment variables are securely injected by the hosting environment rather than hardcoded.

---
## 🚨 Important Deployment Note for Evaluators
**Cloud Run Readiness:** This repository contains a fully configured `Dockerfile` designed for Google Cloud Run deployment. 
**Fallback URL:** Due to persistent regional banking restrictions (RBI mandates) preventing the standard GCP billing verification required to activate Cloud Run, the live preview has been securely hosted on Streamlit Community Cloud. The codebase itself remains 100% Cloud Run ready.

**Live Preview (Fallback):** https://election-assistant-promptwars.streamlit.app/
