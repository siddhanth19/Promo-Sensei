from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import ingest_to_vector_db
import os
from dotenv import load_dotenv
load_dotenv()

db_path='faiss_index'
if not os.path.exists(db_path):
    ingest_to_vector_db.create_vector_store()


embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.load_local("faiss_index", embeddings=embedder,allow_dangerous_deserialization=True)


template = '''
You are an intelligent shopping assistant integrated into Slack. Based strictly on the provided context, respond to the user query by following these instructions:

1. Begin with a short summary (atlest 2–3 lines) highlighting relevant promotions.
2. Then list matching offers using a clean, Slack-friendly text format and make sure to add a category in the details of offer based on the product name.

### Formatting Rules for Slack:
- Only use plain text and Slack-compatible markdown:
  - Use `*bold*` for product names
  - Use `>` for summary blockquotes
  - Use `<URL|View Offer>` for links
- Do NOT use `[text](url)` or `**double asterisks**` as they won’t render correctly in Slack.

---

### User Query:
{input}

---

### Context:
{context}

---

### Output Format:

> Short summary of the result here (at least 2–3 lines)

*Available Offers:*
• *Product Name*  
  Discount: 75% OFF  
  Price: Rs.799  
  Brand: AJIO
  Category: Clothing 
  <https://example.com/offer|View Offer>

• *Another Product*  
  Discount: 60% OFF  
  Price: Rs.499  
  Brand: Puma 
  Category: Shoes
  <https://example.com/puma|View Offer>

If there are no relevant offers in the context, simply return:
*Couldn't find relevant offers.*
'''



prompt=PromptTemplate.from_template(template)

llm=ChatGroq(model='llama-3.3-70b-versatile',temperature=0.0)

model=prompt|llm|StrOutputParser()

def query(input):
    docs=vector_db.similarity_search(query=input,k=5)

    context='\n'.join(doc.page_content for doc in docs)
    res=model.invoke({'input':input,'context':context})
    return res