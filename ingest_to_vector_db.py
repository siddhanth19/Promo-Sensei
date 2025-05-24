from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import scraper
from dotenv import load_dotenv
load_dotenv()

def deal_to_document(deal):
    content = f"""
    Title: {deal['title']}
    Description: {deal['description']}
    Discount: {deal['discount']}
    Price: Rs.{deal['price']}
    Brand: {deal['brand_merchant']}
    URL: {deal['deal_url']}
    """

    metadata = {
        "brand": deal['brand_merchant'],
        "price": deal['price'],
        "discount": deal['discount'],
        "url": deal['deal_url']
    }

    return Document(page_content=content.strip(), metadata=metadata)


def create_vector_store():
    deals=scraper.get_deals()
    docs=[]
    for deal in deals:
        docs.append(deal_to_document(deal))

    embedder=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db=FAISS.from_documents(documents=docs,embedding=embedder)
    vector_db.save_local('faiss_index')


if __name__=='__main__':
    create_vector_store()