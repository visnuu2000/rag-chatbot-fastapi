f = open('rag_engine.py').read() 
f = f.replace('from langchain_community.embeddings import HuggingFaceEmbeddings', 'from langchain_community.embeddings import HuggingFaceEmbeddings') 
open('rag_engine.py', 'w').write(f) 
print('done') 
