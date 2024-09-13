from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import execute_values

model = SentenceTransformer('all-MiniLM-L6-v2')

def encode_and_store_documents(documents):
    conn = psycopg2.connect("dbname=document_retrieval user=your_username password=your_password")
    cur = conn.cursor()

    encodings = model.encode(documents)
    
    data = [(doc, encoding.tolist()) for doc, encoding in zip(documents, encodings)]
    
    execute_values(cur, 
                   "INSERT INTO documents (content, embedding) VALUES %s",
                   data,
                   template="(%s, %s::vector)")

    conn.commit()
    cur.close()
    conn.close()
