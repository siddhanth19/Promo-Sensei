# 🛍️ Promo Sensei — Smart Offer Discovery Assistant

**Promo Sensei** is an intelligent Slack-integrated assistant that scrapes live e-commerce promotions, stores them in a vector database using embeddings, and answers user queries using a RAG (Retrieval-Augmented Generation) pipeline backed by a powerful LLM.

---

## 🚀 Project Overview

Promo Sensei continuously monitors promotional deals from websites like GrabOn, extracts relevant deal information, and responds to user queries via Slack slash commands using natural language.

---

## 🧱 Project Structure
promo_sensei/
├── scraper.py # Scrapes deals from GrabOn
├── ingest_to_vector_db.py # Embeds and stores data in FAISS
├── rag_query.py # RAG pipeline using LangChain + Groq LLM
├── slackbot.py # Slack bot interface using Slack Bolt SDK
├── offers.json # Locally cached deal data (auto-generated)
├── faiss_index/ # FAISS vector store (auto-generated)
├── .env # API keys and environment variables


---

## ⚙️ Setup Instructions

### 1. Clone the repo and install dependencies

uv venv && source .venv/bin/activate    # Or python -m venv venv
uv pip install -r pyproject.toml        # Ensure required packages are installed
playwright install                      # For browser automation

### 2. Create a .env file with your api keys:

SLACK_BOT_TOKEN=your-slack-bot-token
SLACK_APP_TOKEN=your-slack-app-token
GROQ_API_KEY=your-groq-api-key
HF_TOKEN=your-hugging-face-token

### 3. Run the Slack Bot in the virtual environment created

python slackbot.py

*Ensure your bot is installed in your Slack workspace and Socket Mode is enabled.*

## ✨ Slash Commands
Use these commands in Slack (via /promosensei [subcommand]):

Command	                            Description
/promosensei search [query]	        Search for deals matching the user query
/promosensei summary	            Summarize top available offers
/promosensei brand [name]	        Show offers for a specific brand
/promosensei refresh	            Re-scrape data and update vector database

## 💬 Sample Queries & Outputs

### Query
*/promosensei search top offers for women*

### Output
![alt text](<_promosensei search command.png>)

## 🧠 Key Design Decisions
### 1. Web Scraping
playwright.async_api is used to scrape dynamic elements from GrabOn.
Extracted data includes: title, brand, price, discount, and offer URL.

### 2. Vector Store with FAISS
Offers are embedded using all-MiniLM-L6-v2 via HuggingFaceEmbeddings.
Stored in a FAISS index with relevant metadata (brand, price, discount, URL).

### 3. Retrieval-Augmented Generation (RAG)
LangChain's PromptTemplate, FAISS retriever, and ChatGroq (LLama 3.3 70B) power the query system.
Slack-compatible output with structured formatting and markdown-safe rendering.

### 4. Slack Integration
Built using the Slack Bolt SDK with Socket Mode for real-time command handling.
Supports extensible commands and message formatting optimized for Slack markdown.


## 📦 Dependencies

* playwright

* slack_bolt

* langchain

* langchain_community

* langchain_groq

* faiss-cpu

* sentence-transformers

* python-dotenv

* langchain-huggingface

## 📸 Screenshots and Demo

[Demo](https://drive.google.com/drive/folders/1Wei_LkITfjArXu8tGjhDdmIAmmflziox?usp=sharing)