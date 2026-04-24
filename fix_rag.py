from groq import Groq 
import os 
 
content = open('rag_engine.py').read() 
content = content.replace('from langchain_community.embeddings import HuggingFaceEmbeddings', 'from langchain_huggingface import HuggingFaceEmbeddings') 
open('rag_engine.py', 'w').write(content) 
print('done') 
