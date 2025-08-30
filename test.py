
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Example documents
documents = [
    "The Eiffel Tower is in Paris.",
    "The Great Wall of China is visible from space.",
    "Python is a popular programming language."
]

# Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(documents)

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))


query = "Where is the Eiffel Tower?"
query_embedding = model.encode([query])
D, I = index.search(np.array(query_embedding), k=2)  # Retrieve top 2

retrieved_docs = [documents[i] for i in I[0]]
print("Retrieved:", retrieved_docs)

from transformers import pipeline

# Concatenate retrieved docs and query
context = " ".join(retrieved_docs)
prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"

# Use a language model (e.g., GPT-2, GPT-3, or open-source LLM)
generator = pipeline("text-generation", model="gpt2")
result = generator(prompt, max_length=100)
print(result[0]['generated_text'])






