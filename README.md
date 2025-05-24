# 🛍️ Promo Sensei — Smart Offer Discovery Assistant

**Promo Sensei** is an intelligent Slack-integrated assistant that scrapes live e-commerce promotions, stores them in a vector database using embeddings, and answers user queries using a RAG (Retrieval-Augmented Generation) pipeline powered by a state-of-the-art LLM.

---

## 🚀 Project Overview

Promo Sensei continuously monitors promotional deals from websites like [GrabOn](https://www.grabon.in), extracts relevant deal information, and responds to user queries via Slack using natural language.

---

## 🧱️ Project Structure

```bash
promo_sensei/
├── scraper.py               # Scrapes deals from GrabOn
├── ingest_to_vector_db.py   # Embeds and stores data in FAISS
├── rag_query.py             # RAG pipeline using LangChain + Groq LLM
├── slackbot.py              # Slack bot interface using Slack Bolt SDK
├── offers.json              # Locally cached deal data (auto-generated)
├── faiss_index/             # FAISS vector store (auto-generated)
├── .env                     # API keys and environment variables
```

---

## ⚙️ Setup Instructions

### 1. Create Virtual Environment & Install Dependencies

```bash
uv venv && source .venv/bin/activate  # Or: python -m venv venv
uv pip install -r pyproject.toml      # Install all required packages
playwright install                    # Install Playwright browsers
```

### 2. Create a `.env` File with Your API Keys

```env
SLACK_BOT_TOKEN=your-slack-bot-token
SLACK_APP_TOKEN=your-slack-app-token
GROQ_API_KEY=your-groq-api-key
HF_TOKEN=your-hugging-face-token
```

### 3. Run the Slack Bot

```bash
python slackbot.py
```

> ✅ Ensure your bot is installed in your Slack workspace and that **Socket Mode** is enabled.

---

## ✨ Slash Commands

Use these in any Slack channel or DM:

| Command                       | Description                               |
| ----------------------------- | ----------------------------------------- |
| `/promosensei search [query]` | Search for deals matching the user query  |
| `/promosensei summary`        | Summarize top available offers            |
| `/promosensei brand [name]`   | Show offers for a specific brand          |
| `/promosensei refresh`        | Re-scrape data and update vector database |

---

## 💬 Sample Queries & Outputs

### Query:

```bash
/promosensei search top offers for women
```

### Output:

![Alt text] (_promosensei search command.png)

---

## 🧠 Key Design Decisions

### 1. Web Scraping

* Uses `playwright.async_api` to dynamically scrape GrabOn's deal listings.
* Captures: `title`, `brand`, `price`, `discount`, and `destination URL`.

### 2. Vector Store with FAISS

* Embeddings are generated using `all-MiniLM-L6-v2` from HuggingFace.
* Stored using FAISS with searchable metadata: brand, discount, and more.

### 3. Retrieval-Augmented Generation (RAG)

* LangChain handles retrieval with a custom `PromptTemplate`.
* RAG responses powered by **LLama 3.3 70B via Groq API**.
* Slack markdown-compatible outputs for seamless viewing.

### 4. Slack Integration

* Built using Slack Bolt SDK with Socket Mode support.
* Real-time response to slash commands with contextual awareness.

---

## 📦 Dependencies

```text
- playwright
- slack-bolt
- langchain
- langchain-community
- langchain-groq
- langchain-huggingface
- faiss-cpu
- sentence-transformers
- python-dotenv
```

---

## 📸 Screenshots and Demo

[View Demo on Google Drive](https://drive.google.com/drive/folders/1Wei_LkITfjArXu8tGjhDdmIAmmflziox?usp=sharing)

---
