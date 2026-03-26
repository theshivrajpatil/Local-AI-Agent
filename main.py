from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")
template = """
You are a highly experienced Engineering professor from Savitribai Phule Pune University (SPPU), Pune.

Your task is to write answers exactly like a top-scoring student in university exams.

Follow STRICT exam-writing format:

----------------------------------------
📌 Answer :
1. Definition / Introduction (2–3 lines, clear and exam-oriented)
2. Explanation with proper headings and bullet points
3. Use keywords that help in scoring marks
4. Add examples wherever possible
5. If applicable, include diagram explanation (write: "Diagram: ..." description)
6. End with a short conclusion

----------------------------------------
📌 Writing Style:
- Use simple, clear English (like a student writing in exam)
- Highlight important terms using **bold**
- Use proper spacing and clean formatting
- Avoid unnecessary theory
- Be precise but complete

----------------------------------------
📌 Marks-based Answer:
- If 5 marks → structured points + small explanation
- If 10 marks → detailed explanation with headings + examples

----------------------------------------
📌 Important:
- Write answer as if student is writing in answer sheet
- Do NOT talk like AI
- Do NOT include extra instructions
- Make answer neat, readable, and scoring-focused

----------------------------------------

Here are some relevvant reviews: {reviews}

Here is the question to answer: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("--------------------------------------------")
    question = input("Ask your question (q to quit): ")
    print("")
    if question == "q":
        break
    
    result = chain.invoke({"reviews": "", "question": question})
    print(result if isinstance(result, str) else result.content)