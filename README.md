# smartknowledge-ai
SmartKnowledge AI – Multimodal AI Assistant

SmartKnowledge AI is a production-style multimodal AI assistant that enables users to interact with an AI system using text, voice, and documents (PDFs).
The application combines LLMs, Retrieval-Augmented Generation (RAG), speech processing, authentication, and persistent chat history into a single cohesive AI product.


✨ Key Features

🔐 Secure user authentication (Signup & Login)

💬 ChatGPT-style conversational interface

📄 PDF upload & document-based question answering (RAG with FAISS)

🧠 Context-aware responses using Large Language Models

🎙 Voice input (Speech-to-Text)

🔊 Voice output (Text-to-Speech)

💾 Persistent chat history stored in database

📥 Downloadable chat history

🎨 Modern UI with custom CSS and responsive layout


🛠 Tech Stack

Frontend: Streamlit

Backend: Python

AI / NLP: Large Language Models (LLMs), FAISS, Retrieval-Augmented Generation (RAG)

Speech: gTTS (Text-to-Speech), Speech Recognition

Database: SQLite

Authentication: Custom username/password system

📂 Project Structure
├── app.py              # Main Streamlit application
├── llm.py              # LLM response generation
├── pdf_rag.py          # PDF loading, chunking, FAISS indexing, RAG
├── voice_input.py      # Speech-to-text processing
├── auth.py             # User authentication logic
├── chat_db.py          # Chat history storage & retrieval
├── database.py         # Database initialization
├── requirements.txt
└── README.md


⚙️ Installation & Setup
# Clone the repository
git clone https://github.com/your-username/smartknowledge-ai.git
cd smartknowledge-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

🧠 How It Works

User signs up or logs in securely

Questions can be asked via text or voice

Optional PDF upload enables document-grounded answers

RAG pipeline retrieves relevant PDF chunks using FAISS

LLM generates context-aware responses

Chat history is saved and can be downloaded

🏗️ System Architecture Overview
User
 │
 │ (Text / Voice / PDF)
 ▼
Streamlit UI (Frontend)
 │
 ├── Authentication Module
 │     └── Login / Signup
 │
 ├── Chat Interface
 │     ├── Text Input
 │     └── Voice Input (Speech-to-Text)
 │
 ├── PDF Processing (Optional)
 │     ├── PDF Text Extraction
 │     ├── Text Chunking
 │     └── FAISS Vector Index
 │
 ├── RAG Pipeline
 │     ├── Retrieve Relevant Chunks
 │     └── Inject Context into LLM
 │
 ├── LLM Engine
 │     └── Context-aware Answer Generation
 │
 ├── Voice Output (Optional)
 │     └── Text-to-Speech (gTTS)
 │
 └── Database Layer
       ├── User Credentials
       └── Chat History


🎯 Use Cases

AI-powered document assistant

Voice-enabled AI chatbot

Knowledge retrieval system for PDFs

Personal or enterprise AI assistant

🚀 Future Enhancements

JWT-based authentication

Cloud deployment (AWS / Azure / GCP)

Multi-language voice support

User roles & subscription plans

👩‍💻 Author

Pathan Feeza
Aspiring AI / GenAI Engineer

⭐ If you find this project useful, feel free to star the repository!
