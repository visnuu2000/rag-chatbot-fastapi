import re 
content = open('rag_engine.py').read() 
content = content.replace('from langchain_community.embeddings import HuggingFaceEmbeddings', 'from langchain_community.embeddings.fastembed import FastEmbedEmbeddings') 
content = content.replace('HuggingFaceEmbeddings(', 'FastEmbedEmbeddings(') 
content = content.replace('model_name="all-MiniLM-L6-v2"', 'model_name="BAAI/bge-small-en-v1.5"') 
open('rag_engine.py', 'w').write(content) 
print('rag_engine.py fixed!') 
