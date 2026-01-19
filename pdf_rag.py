from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- PDF TEXT EXTRACTION ----------------
def load_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# ---------------- SPLIT TEXT INTO CHUNKS ----------------
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# ---------------- CREATE FAISS INDEX ----------------
def create_faiss_index(chunks):
    embeddings = embedding_model.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, chunks

# ---------------- GET ANSWER FROM PDF ----------------
def get_pdf_answer(question, index, chunks, llm_function):
    q_embedding = embedding_model.encode([question])
    
    # Search top 3 chunks
    scores, indices = index.search(np.array(q_embedding), k=3)

    relevant_chunks = []
    for i, score in enumerate(scores[0]):
        if score <= 1.0:  # similarity threshold
            relevant_chunks.append(chunks[indices[0][i]])

    if not relevant_chunks:
        return "This information is not mentioned in the provided PDF."

    combined_chunk = "\n".join(relevant_chunks)

    prompt = f"""
You are an AI assistant. STRICTLY follow these rules:

- Use ONLY the PDF content below.
- Provide a clear, detailed answer.
- Do NOT use any outside knowledge.
- If the answer is not explicitly stated, reply exactly:
  "This information is not mentioned in the provided PDF."

PDF CONTENT:
{combined_chunk}

Question:
{question}

Answer:
"""

    return llm_function(prompt, [])
