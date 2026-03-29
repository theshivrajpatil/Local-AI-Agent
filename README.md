# WhatsApp AI Study Assistant (RAG-Based)
This project is an AI-powered study assistant that integrates with WhatsApp. It allows users to upload study materials such as PDFs, PowerPoint presentations, Excel sheets, and CSV files, and then ask questions based on those documents.

The system uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate and structured answers based on the uploaded content. It is designed to help engineering students study more effectively using their own notes.

## Features
- WhatsApp-based interaction using Twilio
- Upload documents directly through chat
- Supports multiple file formats:
  - PDF
  - PPT / PPTX
  - Excel (XLS/XLSX)
  - CSV
- Automatic document processing and embedding
- Semantic search using vector database (ChromaDB)
- Local language model using Ollama (Llama3 or Mistral)
- Structured, exam-oriented responses
- Retrieval-Augmented Generation (RAG) architecture

## How It Works

1. User uploads a document via WhatsApp  
2. The system processes the file and extracts text  
3. Text is split into smaller chunks  
4. Each chunk is converted into embeddings  
5. Embeddings are stored in a vector database (ChromaDB)  

When a user asks a question:
- Relevant chunks are retrieved from the database  
- Context is passed to the language model  
- The model generates a structured answer 

## System Architecture

The system follows a standard RAG workflow:
1. User uploads a document    
2. The document is loaded and split into smaller chunks  
3. Chunks are converted into embeddings  
4. Embeddings are stored in ChromaDB  
5. When a question is asked:
   - Relevant chunks are retrieved  
   - Context is passed to the language model  
   - The model generates a structured answer  

## Technologies Used

- Python   
- LangChain  
- Ollama (Local LLM)  
- ChromaDB (Vector Store)  
- Unstructured (Document parsing) 