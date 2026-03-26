from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

model = OllamaLLM(model="llama3.2")
# Load vector database
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db = Chroma(persist_directory="./chrome_langchain_db", embedding_function=embeddings)

template = """
You are an expert SPPU Engineering professor.

Answer the question using the given context from student notes.

Write the answer in proper exam format like a top-scoring student.

Structure:
1. Definition / Introduction (2–3 lines)
2. Explanation with clear headings and bullet points
3. Include examples (especially SQL syntax if applicable)
4. Add "Diagram:" description only if needed
5. End with a short conclusion

Rules:
- Do NOT repeat instructions
- Do NOT mention words like "Definition / Introduction" explicitly
- Do NOT explain what you are doing
- Give direct, clean, exam-ready answer
- Avoid unnecessary theory
- Use simple English

Context:
{context}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("--------------------------------------------")
    question = input("Ask your question (q to quit): ")

    if question == "q":
        break
    
    # Retrieve relevant documents from vector DB
    docs = db.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    result = chain.invoke({
        "question": question,
        "context": context
    })
    output = result if isinstance(result, str) else result.content

    print("\n📘 Answer:\n")
    print(output.strip())
    print("\n" + "-"*50)