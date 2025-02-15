from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from scrap.disease_outbreak_scrap import disease_outbreak_scrap
from scrap.fact_sheet_scrap import fact_sheet_scrap
from scrap.question_answer_scrap import question_answer_scrap
#RAG function 
def rag():
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    loader = TextLoader("./info.txt")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=800)
    splits = text_splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(splits, embeddings)

    return vectorstore

if __name__ == "__main__":
    disease_outbreak_scrap()
    fact_sheet_scrap()
    question_answer_scrap()