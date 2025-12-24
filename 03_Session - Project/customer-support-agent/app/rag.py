from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from app.utils import get_embeddings
import os

def load_documents(directory="data/"):
    loader = DirectoryLoader(directory, glob="**/*.*", loader_cls=TextLoader, silent_errors=True)
    pdf_loader = DirectoryLoader(directory, glob="**/*.pdf", loader_cls=PyPDFLoader)

    docs = loader.load() + pdf_loader.load()
    return docs

def build_rag_index():
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(docs)
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

def get_retriever():
    embeddings = get_embeddings()
    if os.path.exists("faiss_index"):
        return FAISS.load_local("faiss_index", embeddings,
                                allow_dangerous_deserialization=True).as_retriever()
    else:
        return build_rag_index().as_retriever()
    
