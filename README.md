# Debate Bot API

FastAPI service that starts a debate, **picks a topic + stance** on the first user message, and **sticks to it**.  
Conversation history is stored **in memory** (no external DB).

---

## Project Layout
```
app/
  __init__.py
  main.py          # FastAPI app entrypoint (app.main:app)
  controller.py    # /debate endpoint
  service.py       # DebateService
  repository.py    # in-memory repository
  models.py
  llm_engine.py    # Groq (optional) or mock engine
  properties.py    # loads .env
tests/
  test_controller.py
  test_repository.py
  test_llm_engine_simple.py
Dockerfile
docker-compose.yml
Makefile
```

---

## Environment

Create a `.env` in the repo root:

```env
PORT=8000
# Optional: if unset, engine uses mock responses (no network)
GROQ_API_KEY=your_groq_api_key_here
```
---

## Quickstart (Local)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run API
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
# Docs: http://localhost:8000/docs
```

---

## Quickstart (Docker)

```bash
# .env must be next to docker-compose.yml
docker compose up -d --build
docker compose logs -f debate-api
# Confirm mapped port:
docker compose port debate-api 8000
```

The container listens on **8000**; host port is `${PORT:-8000}` from `.env`.

---

## Makefile Shortcuts

```bash
make install   # docker compose build
make run       # docker compose up -d --build
make test      # run tests inside the container (requires pytest in image)
make down      # docker compose down
make clean     # down -v --rmi local --remove-orphans
```

---

## API

**POST `/debate`**

**Request**
```json
{
  "conversation_id": "text or null",
  "message": "text"
}
```

**Response**
```json
{
  "conversation_id": "text",
  "message": [
    {"role": "user", "message": "text"},
    {"role": "bot",  "message": "text"}
  ]
}
```

**Example**
```bash
curl -s -X POST http://localhost:8000/debate   -H 'Content-Type: application/json'   -d '{"conversation_id": null, "message": "Let’s talk about nuclear energy"}'
```

---

## Tests

```bash
pytest -q                 # run from repo root
# or via Docker:
docker compose run --rm debate-api pytest -q
```

If imports fail in tests, add a `pytest.ini` in the repo root:

```ini
[pytest]
pythonpath = .
```

---

## Get & Configure a Groq API Key (optional)

1. Open the Groq Console: https://console.groq.com/  
2. Create a key in **API Keys**: https://console.groq.com/keys  
3. Put it in `.env`:
   ```env
   GROQ_API_KEY=sk_********************************
   ```
4. Start the app. You should see: `LLM Engine initialized with Groq`.  
   If not set, the engine stays in **mock mode**.

---

## Troubleshooting (Quick)

- **`ModuleNotFoundError: app`** → ensure `app/__init__.py` exists and run from the repo root.  
- **Tests don’t find `app`** → use `pytest.ini` with `pythonpath = .`.  
- **Port not listening** → check logs `docker compose logs -f debate-api` and open `http://localhost:${PORT}`.
