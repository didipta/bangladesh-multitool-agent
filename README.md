# 🇧🇩 Bangladesh Multi-Tool AI Agent

A Bangladesh-focused **AI agent** that intelligently selects the right tool to answer questions about hospitals, educational institutions, restaurants, and general/current information.

The project combines **LangChain, Google Gemini, SQLite, SQL, Tavily Web Search, Hugging Face datasets, and Streamlit** into one conversational AI application.

---

## 🌐 Live Demo

🚀 **Try the Bangladesh Multi-Tool AI Agent online:**

**Live Application:** https://bangladesh-multitool-agent.onrender.com/

The deployed application provides access to the Bangladesh-focused AI agent without requiring a local installation. Users can ask questions about hospitals, educational institutions, restaurants, and general/current information.


## ✨ Features

- 🤖 AI-powered conversational interface
- 🧠 Intelligent tool selection with LangChain
- 🏥 Bangladesh hospital database search
- 🏛️ Bangladesh institution database search
- 🍽️ Bangladesh restaurant database search
- 🌐 Web search for general and current information
- 🗄️ SQLite databases for structured data
- 💬 Conversation history / follow-up questions
- 📊 Natural-language questions over SQL data
- 🇧🇩 Bangladesh-focused responses
- 🐳 Docker-ready deployment

---

## 🏗️ Project Structure

```text
bangladesh-multitool-agent/
│
├── databases/
│   ├── hospitals.db
│   ├── institutions.db
│   └── restaurants.db
│
├── scripts/
│   └── ...
│
├── tools/
│   ├── __init__.py
│   ├── hospitals_tool.py
│   ├── institutions_tool.py
│   ├── restaurants_tool.py
│   ├── sql_tool_base.py
│   └── web_search_tool.py
│
├── .env
├── .gitignore
├── agent.py
├── Dockerfile
├── README.md
└── requirements.txt
```

> If your SQLite files are currently stored somewhere else, update the database paths in the corresponding tool files and keep the README structure consistent with your actual repository.

---

## 🔧 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangChain | AI agent and tool orchestration |
| Google Gemini | Large language model |
| SQLite | Structured Bangladesh datasets |
| SQL | Database querying |
| Tavily | Web search |
| Streamlit | Web interface |
| Hugging Face Datasets | Dataset source |
| Docker | Containerization |

---

## 🧠 How It Works

The application receives a natural-language question and allows the AI agent to select the most appropriate tool.

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Streamlit UI    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Gemini +        │
                         │  LangChain Agent │
                         └────────┬─────────┘
                                  │
               ┌──────────────────┼──────────────────┐
               │                  │                  │
               ▼                  ▼                  ▼
       ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
       │ Institutions │   │   Hospitals  │   │ Restaurants  │
       │   DB Tool    │   │    DB Tool   │   │    DB Tool   │
       └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
              │                  │                  │
              ▼                  ▼                  ▼
       institutions.db    hospitals.db     restaurants.db

                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Web Search Tool │
                         │     (Tavily)     │
                         └──────────────────┘
```

### Example routing

**Question:**

> How many hospitals are in Dhaka?

➡️ `HospitalsDBTool`

**Question:**

> Find colleges in Chattogram.

➡️ `InstitutionsDBTool`

**Question:**

> Find restaurants in Dhanmondi.

➡️ `RestaurantsDBTool`

**Question:**

> What is the role of DGHS in Bangladesh?

➡️ `WebSearchTool`

The agent should use the database tools for questions that can be answered from the local datasets instead of unnecessarily searching the web.

---

## 📊 Data Sources

This project is designed around Bangladesh-specific structured datasets hosted on Hugging Face.

### Institutions

`Mahadih534/Institutional-Information-of-Bangladesh`

Used for information such as:

- Institution name
- EIIN
- Institution type
- Division
- District
- Upazila / Thana
- Union
- Area
- Address
- Management type
- Student type
- Education level
- Affiliation
- MPO status

### Hospitals

`Mahadih534/all-bangladeshi-hospitals`

The hospital dataset includes fields such as:

- ID
- Name
- Bangla name
- Code
- Agency
- Type
- Division
- District
- City Corporation
- Upazila
- Paurasava
- Union
- Private

**Important:** Do not claim that the hospital dataset contains beds, doctors, phone numbers, facilities, or departments unless those fields are actually present in the database.

### Restaurants

`Mahadih534/Bangladeshi-Restaurant-Data`

The restaurant tool uses the local SQLite copy of the restaurant dataset.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd bangladesh-multitool-agent
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

`TAVILY_API_KEY` is required only if web search is enabled by your application.

**Never commit `.env` or API keys to GitHub.**

---

## 🗄️ Database Setup

The application expects three SQLite databases:

```text
databases/
├── institutions.db
├── hospitals.db
└── restaurants.db
```

Make sure the database paths used by:

```text
tools/institutions_tool.py
tools/hospitals_tool.py
tools/restaurants_tool.py
```

match the actual location of your `.db` files.

You can inspect a SQLite database with:

```bash
sqlite3 databases/hospitals.db
```

Then:

```sql
.tables
.schema hospitals
```

If your database-generation script is available, run it before starting the application.

---

## ▶️ Run Locally

Start the Streamlit application:

```bash
streamlit run agent.py
```

Then open the local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

---

## 🐳 Run with Docker

### Build the image

```bash
docker build -t bangladesh-multitool-agent .
```

### Run the container

Windows PowerShell:

```powershell
docker run --rm -p 8501:8501 `
  -e GOOGLE_API_KEY="your_google_api_key" `
  -e TAVILY_API_KEY="your_tavily_api_key" `
  bangladesh-multitool-agent
```

macOS / Linux:

```bash
docker run --rm -p 8501:8501 \
  -e GOOGLE_API_KEY="your_google_api_key" \
  -e TAVILY_API_KEY="your_tavily_api_key" \
  bangladesh-multitool-agent
```

Open:

```text
http://localhost:8501
```

### Using an `.env` file with Docker

If your Docker version supports environment files:

```bash
docker run --rm -p 8501:8501 --env-file .env bangladesh-multitool-agent
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---:|---|
| `GOOGLE_API_KEY` | Yes | Google Gemini API key |
| `TAVILY_API_KEY` | Optional* | Tavily API key for web search |

\* Required when `WebSearchTool` is enabled and expects Tavily.

---

## 💬 Example Questions

### 🏥 Hospitals

```text
How many hospitals are in Dhaka?
```

```text
List hospitals in Chattogram.
```

```text
How many private hospitals are in Sylhet?
```

```text
Show hospitals in Rajshahi.
```

### 🏛️ Institutions

```text
How many institutions are in Dhaka?
```

```text
Find colleges in Uttara.
```

```text
List schools in Chattogram.
```

```text
How many institutions are in Sylhet?
```

### 🍽️ Restaurants

```text
Find restaurants in Dhanmondi.
```

```text
List restaurants in Gulshan.
```

```text
How many restaurants are in Dhaka?
```

### 🌐 Web Search

```text
What is the role of DGHS in Bangladesh?
```

```text
What are the divisions of Bangladesh?
```

```text
What is the capital of Bangladesh?
```

---

## 🔄 Conversational Follow-up

The agent is designed to understand follow-up questions using conversation history.

Example:

```text
User:
How many hospitals are in Dhaka?

Assistant:
[Dhaka hospital count]

User:
What about Chattogram?

Assistant:
[Chattogram hospital count]
```

The second question should be interpreted in the context of the first question.

---

## 🛠️ Tools

### `InstitutionsDBTool`

Queries the institutions SQLite database using natural-language questions.

### `HospitalsDBTool`

Queries the hospitals SQLite database.

### `RestaurantsDBTool`

Queries the restaurant SQLite database.

### `WebSearchTool`

Uses Tavily for general, current, or web-based information that is not available in the local datasets.

### `sql_tool_base.py`

Contains shared SQL/database logic used by the database tools.

---

## 🧪 Recommended Testing

Test each tool independently before testing the complete agent.

### Hospital test

```text
How many hospitals are in Dhaka?
```

### Institution test

```text
How many institutions are in Dhaka?
```

### Restaurant test

```text
Find restaurants in Dhanmondi.
```

### Web test

```text
What is the role of DGHS?
```

### Follow-up test

```text
How many hospitals are in Dhaka?
What about Chattogram?
```

---

## 🛡️ Security

Do not commit secrets.

Your `.gitignore` should include:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

If API keys are accidentally pushed to GitHub, revoke and regenerate them immediately.

---

## 📦 Production Notes

For production deployment:

1. Store API keys in environment variables or a secret manager.
2. Do not expose `.env`.
3. Keep SQLite databases read-only if the application only performs searches.
4. Add logging and monitoring.
5. Pin dependency versions for reproducible builds.
6. Consider a production database such as PostgreSQL if the dataset or traffic grows significantly.
7. Run the application behind a reverse proxy or managed hosting platform when appropriate.

---

## 🐳 Docker Health Check

The Docker image includes a Streamlit health check:

```text
/_stcore/health
```

You can check the running container with:

```bash
docker ps
```

For container logs:

```bash
docker logs <container_id>
```

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/my-feature
```

3. Commit your changes.

```bash
git add .
git commit -m "Add my feature"
```

4. Push the branch.

```bash
git push origin feature/my-feature
```

5. Open a Pull Request.

---

## 📄 License

Add your preferred project license here, for example MIT.

If this project is submitted as an academic or technical assignment, follow the license and attribution requirements specified by the assignment.

---

## 👨‍💻 Author

**Dipta Saha**

Software Engineer | Frontend & AI Application Development

Built with ❤️ in Bangladesh 🇧🇩

---

## ⭐ Project Highlights

- Multi-tool AI agent
- Natural-language SQL querying
- Bangladesh-specific datasets
- Gemini-powered reasoning
- LangChain tool orchestration
- Web search integration
- Streamlit conversational UI
- SQLite data layer
- Docker containerization

If you find the project useful, consider giving the repository a ⭐ on GitHub.
