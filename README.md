# 🗳️ CivicSync: Your Election Assistant

## 📌 What I Built
I chose the **Election Process Education** vertical. The goal was simple: voting can be confusing, so I built a non-partisan, easy-to-use AI assistant that helps people understand how to register, what to bring, and who represents them locally. 

## 🧠 How It Works Behind the Scenes
I wanted to combine conversational AI with real-world, local data. Here is how I put it together:

1. **The AI Brain (Gemini 2.5 Flash):** I specifically upgraded to the **Gemini 2.5 Flash** model to take advantage of its January 2025 knowledge cutoff, ensuring it understands the most recent election laws. I gave it a strict system prompt to keep it strictly neutral and non-partisan. I also baked in Google's `SafetySettings` to automatically block any harassment or hate speech, and tweaked the `GenerationConfig` to keep the answers factual and concise.

2. **The Local Data (Google Civic API):** To make it personal, users can enter their address to look up their local representatives using the Google Civic Information API. 
   *💡 Fun hackathon hurdle:* I discovered the specific `v2/representatives` endpoint was officially deprecated in April 2025! Instead of letting the app crash with a raw 404 error, I built a custom error-handler that catches this edge case and gracefully explains the deprecation to the user.

## ⚙️ The Tech Stack & Upgrades
* **Frontend:** Built with Streamlit. I focused heavily on **Accessibility** by adding high-contrast text, tooltips, and ARIA-friendly placeholders so screen readers can easily navigate the app.
* **The SDK:** Migrated entirely to the new, official `google-genai` Python SDK to avoid legacy deprecation warnings.
* **Performance:** Implemented `st.cache_resource` and session states to stop the app from re-running API calls on every keystroke, preventing UI freezes. 
* **Logging:** Hooked up `google-cloud-logging` to track errors cleanly in a production environment.

## ✅ Testing & Reliability
I didn't just test the "happy paths." To make sure the app doesn't break under pressure, I wrote a full test suite using `pytest`. I also used `unittest.mock` to simulate API failures, server timeouts (503s), and empty user inputs to guarantee the app fails gracefully no matter what. 

---
## 🚨 Note to the Judges: Deployment & Cloud Run
This repository includes a fully configured `Dockerfile` exposing port 8080, meaning the code is **100% ready for Google Cloud Run**. 

However, due to current regional banking restrictions (RBI mandates in India) blocking my Google Cloud billing verification, I couldn't spin up the Cloud Run instance today. To make sure you can still interact with the app, I've deployed a live fallback version using Streamlit Community Cloud.

**Live Preview:** https://election-assistant-promptwars.streamlit.app/
