from openai import OpenAI
from dotenv import load_dotenv
import os
from retriever import search

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask(question):
    chunks = search(question)
    
    if not chunks:
        return "Sorry, I couldn't find relevant information in the knowledge base."
    
    context = "\n\n".join([
        f"Source: {c['source']}\n{c['content']}"
        for c in chunks
    ])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"""You are a helpful assistant. Answer the user's question using ONLY the context below.
The question may use different words than the context (e.g. "money back" means "refund").
If the context contains relevant information, use it to answer even if the wording differs.
Only say "I cannot confirm this from the knowledge base." if the context is truly unrelated.
Always end your answer with the source in format [source].

Context:
{context}

Question: {question}"""
        }]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    questions = [
        "What is the refund policy?",
        "How can I get my money back?",
        "Under which condition I can get my money back?",
    ]
    for q in questions:
        print(f"\n❓ {q}")
        print(ask(q))