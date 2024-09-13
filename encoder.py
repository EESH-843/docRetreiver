from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def encode_text(text: str) -> np.ndarray:
    return model.encode(text)

async def encode_and_store_documents(db, documents: list[str]):
    encodings = model.encode(documents)
    
    async with db.transaction():
        await db.executemany(
            "INSERT INTO documents (content, embedding) VALUES ($1, $2)",
            [(doc, encoding.tolist()) for doc, encoding in zip(documents, encodings)]
        )
