# Contributing to ProdSynth

## Development Setup

```bash
git clone https://github.com/homgorn/prodsynth-monorepo.git
cd prodsynth-monorepo

# Backend
cd apps/backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Frontend
cd apps/frontend
npm install

# Run all services
cd ../..
docker-compose up -d  # Neo4j, Redis, PostgreSQL, Loki, Grafana
```

## Testing

### Backend (pytest)
```bash
cd apps/backend
pip install pytest pytest-asyncio pytest-cov httpx
pytest ../tests/unit -v
pytest ../tests/integration -v --tb=short
```

### Frontend (Vitest)
```bash
cd tests
npm install
npx vitest run
```

### Load Testing (k6)
```bash
k6 run tests/load/api-load-test.js
```

## Code Style

- **Python:** Black formatter, isort, Ruff linter
- **TypeScript:** Prettier, ESLint
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`)

## Project Structure

```
prodsynth-monorepo/
├── apps/
│   ├── backend/          # FastAPI + gRPC
│   └── frontend/         # Next.js 14
├── packages/
│   ├── agents/          # 12 synthesis agents
│   ├── core/            # Synthesis engine + debug utils
│   ├── graph/           # Graphiti adapter
│   └── models/          # Shared Pydantic models
├── tests/
│   ├── unit/            # Unit tests (pytest)
│   ├── integration/      # API + graph tests
│   └── load/            # k6 load tests
├── docs/                # Architecture docs
└── specs/               # OpenAPI 3.1, Protobuf
```

## Pull Request Process

1. Create feature branch: `git checkout -b feat/my-feature`
2. Write tests first (TDD approach)
3. Ensure all tests pass: `pytest` + `vitest`
4. Run linting: `ruff check .` + `eslint .`
5. Commit with conventional message
6. Open PR with description

## Running the App

```bash
# Backend
cd apps/backend
uvicorn main:app --reload --port 8000

# Frontend
cd apps/frontend
npm run dev

# Or Docker
docker-compose up -d
```

## Debugging

- Backend logs: `docker-compose logs backend -f`
- Frontend logs: `docker-compose logs frontend -f`
- Neo4j browser: http://localhost:7474
- Grafana: http://localhost:3001
- API docs: http://localhost:8000/docs