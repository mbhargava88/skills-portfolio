# SmartCart AI 🛒

SmartCart AI is an LLM-powered product recommendation engine built with Clean Architecture and Domain-Driven Design (DDD). It uses Groq for reasoning and a Vector Store for retrieval-augmented generation (RAG) concepts.

## 🏗 Architecture

The project follows a strict strict separation of concerns:

- **Domain Layer** (`src/domain`): Entities (`Product`, `Order`, `Cart`) and Interfaces. No external dependencies.
- **Application Layer** (`src/application`): Use cases (`RecommendationService`). Orchestrates logic.
- **Infrastructure Layer** (`src/infrastructure`): Implementations (CSVLoader, ChromaVectorStore, GroqClient). External adapters.
- **Interface Layer** (`src/interface`): Streamlit UI. Entry point.

## 🚀 Setup & Run

### Prerequisites
- Python 3.10+
- Poetry
- Groq API Key (get one at console.groq.com)

### Quick Start
1. **Clone the repo**
2. **Install dependencies**:
   ```bash
   make install
   ```
3. **Run the App**:
   ```bash
   export GROQ_API_KEY=your_key_here
   make run
   ```
   Or use the UI sidebar to input the key.

### Docker
```bash
docker-compose up --build
```

## 🧪 Testing
Run the unit tests:
```bash
make test
```

## 🧠 AI Strategy
- **Data Source**: `orders.csv` (History) and `products.csv` (Catalog).
- **Retrieval**: Uses Product ID lookup (and placeholders for Vector Search).
- **Reasoning**: Groq LLM takes user history + cart context -> Explains recommendations.

## 📖 Documentation

For a detailed walkthrough of the implementation and validation, see [WALKTHROUGH.md](WALKTHROUGH.md).
