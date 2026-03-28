# app.py

from flask import Flask, request
import requests
import os

# Import from your existing rag.py
from rag import db, load_file, embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config['SERVER_NAME'] = None
app.config['PREFERRED_URL_SCHEME'] = 'https'

UPLOAD_FILE = "uploaded_file"

# 🔥 Process uploaded file dynamically
def process_file(file_path):
    docs = load_file(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    split_docs = splitter.split_documents(docs)
    db.add_documents(split_docs)


# 🔥 Ask question using vector DB
def ask_question(question):
    docs = db.similarity_search(question, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an engineering professor.

Answer clearly in exam format.

Context:
{context}

Question:
{question}

Answer:
"""

    # Using Ollama via embeddings model (LLM needed)
    from langchain_ollama.llms import OllamaLLM
    model = OllamaLLM(model="llama3")

    return model.invoke(prompt)


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    message = request.form.get("Body")
    media_url = request.form.get("MediaUrl0")
    media_type = request.form.get("MediaContentType0")

    # 📄 File upload
    if media_url:
        try:
            ext = ".pdf"

            if media_type:
                if "pdf" in media_type:
                    ext = ".pdf"
                elif "presentation" in media_type:
                    ext = ".pptx"
                elif "sheet" in media_type:
                    ext = ".xlsx"
                elif "csv" in media_type:
                    ext = ".csv"

            file_path = UPLOAD_FILE + ext

            file_data = requests.get(media_url).content
            with open(file_path, "wb") as f:
                f.write(file_data)

            process_file(file_path)

            resp = MessagingResponse()
            resp.message("File uploaded and processed successfully.")
            return str(resp)

        except Exception as e:
            resp = MessagingResponse()
            resp.message(f"Error processing file: {str(e)}")
            return str(resp)

    # 💬 Question
    if message:
        try:
            answer = ask_question(message)
            resp = MessagingResponse()
            resp.message(answer)
            return str(resp)

        except Exception as e:
            resp = MessagingResponse()
            resp.message(f"Error generating answer: {str(e)}")
            return str(resp)

    resp = MessagingResponse()
    resp.message("No input received.")
    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)