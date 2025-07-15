# DevBuddy 🧑‍💻📘

DevBuddy is your personal developer assistant built to simplify documentation. Instead of endlessly searching docs, manually checking for deprecations, or copying boilerplate code, just paste a URL — DevBuddy will crawl the site, convert its content to markdown, and power an intelligent chatbot that gives you instant, accurate, and context-aware answers.

Just provide a URL, and DevBuddy will:

- 🌐 Crawl the documentation site  
- 📝 Convert its content into markdown  
- 🔍 Perform Retrieval-Augmented Generation (RAG)  
- 🤖 Answer your queries in real-time

---

## 🚀 Features

- 🔗 **URL-based Crawling** – Paste a doc URL, and DevBuddy handles crawling via `crawl4ai`.
- 📄 **Auto Markdown Conversion** – Extracted content is converted to clean markdown for vector indexing.
- 🔍 **RAG-based Search** – Combines document retrieval with generative AI for precise, contextual answers.
- 💬 **AI-Powered Chatbot** – Get instant, code-aware replies tailored to your documentation.
- ⚙️ **Boilerplate Generator** – Generate code snippets based on your query and the indexed docs.
- ⚡ **One-Click Setup** – No need to upload markdowns or documents manually.

---

## 🧰 Tech Stack

| Component   | Stack                                  |
|------------|-----------------------------------------|
| Frontend   | React, TailwindCSS                      |
| Backend    | FastAPI                                 |
| Crawling   | `crawl4ai`                              |
| Vector DB  | FAISS                                   |
| LLM        | Gemini 2.0 Flash *(swappable: OpenAI, Claude)* |
| RAG Engine | Custom-built: Chunking + Semantic Search|

---

## 🧪 How It Works

1. You enter a documentation website URL.
2. DevBuddy crawls the site using a BFS strategy via `crawl4ai`.
3. Content is converted to markdown with `DefaultMarkdownGenerator`.
4. The markdown is embedded and stored in a FAISS vector DB.
5. The chatbot answers your queries using a custom RAG pipeline.

> 💡 Example:  
> **"Hey DevBuddy, how do I set up authentication in Supabase?"**  
> → DevBuddy returns the precise snippet and explanation from Supabase docs.

---

## 📁 Monorepo Structure

```

DevBuddy/
├── frontend/         # React + Tailwind client
├── backend/          # FastAPI backend & CLI tools
├── main.py           # Entry point (if any)
├── requirements.txt  # Backend Python deps
├── .gitignore
└── README.md         # You're here

```

---

## 🛠️ Setup Instructions

### 🔗 Environment Variables
Create a `.env` file in the root:

```

GOOGLE_API_KEY=your_gemini_key

````

---

### 📦 Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Unix
pip install -r requirements.txt
uvicorn devbuddy_api:app --reload
````

---

### 💻 Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

---

## 🧠 Coming Soon

* 🔁 LLM switching: Gemini / OpenAI / Claude
* 🔍 Source highlighting in chatbot answers
* 🌐 Multi-site documentation merging & unified querying

---

## 🤝 Contributing

Contributions are welcome!
Feel free to open issues, submit PRs, or suggest new features.

Built with ❤️ by [Sanjay Biju](https://github.com/sanislearning)
