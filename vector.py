from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPowerPointLoader, CSVLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

# --- Support for multiple file types ---
documents = []

def load_file(file_path):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".ppt") or file_path.endswith(".pptx"):
        loader = UnstructuredPowerPointLoader(file_path)
    elif file_path.endswith(".csv"):
        loader = CSVLoader(file_path)
    elif file_path.endswith(".xls") or file_path.endswith(".xlsx"):
        loader = UnstructuredExcelLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    return loader.load()

# Example usage (you can replace with dynamic input later)
folder_path = "./data"

if os.path.exists(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            docs = load_file(file_path)
            documents.extend(docs)
        except Exception as e:
            print(f"Skipping {file}: {e}")

# --- Split documents into smaller chunks to avoid context length error ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

split_docs = text_splitter.split_documents(documents)

if add_documents and split_docs:
    db = Chroma.from_documents(split_docs, embeddings, persist_directory=db_location)
else:
    db = Chroma(persist_directory=db_location, embedding_function=embeddings)