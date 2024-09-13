from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example document embeddings
docs = ["Document 1 text", "Document 2 text"]
doc_embeddings = model.encode(docs)

# Initialize the FAISS index
index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(np.array(doc_embeddings).astype(np.float32))

# Function to search for documents
def search(query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding).astype(np.float32), top_k)
    return indices, distances
