import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def get_pdf_text(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

def get_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100
    )
    return splitter.split_text(text)

def get_vectorstore(chunks):
    embeddings = FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore

def get_answer(vectorstore, question):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )
    prompt = PromptTemplate(
        template="""You are a helpful assistant. \
Use the context below to answer the question. \
Be detailed and specific in your answer. \
If the answer is truly not in the context, \
say 'Answer not found in the document.'

Context:
{context}

Question:
{question}

Answer:""",
        input_variables=["context", "question"]
    )
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )
    def format_docs(docs):
        return "\n\n".join(
            doc.page_content for doc in docs
        )
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke(question)

def debug_pdf(pdf_file):
    text = get_pdf_text(pdf_file)
    return f"Extracted {len(text)} characters. First 200 chars: {text[:200]}"