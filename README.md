Random Number API
=================
FastAPI service exposing `GET /random` (JSON random number) and `GET /health`.

Local Run
---------
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
TMPDIR=/tmp python -m pytest      # workaround for WSL temp path issues
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Docker
------
```bash
docker build -t random-number-api .
docker run -p 8000:8000 random-number-api
```

CI/CD
-----
- Workflow: `.github/workflows/ci.yml`
- Pushes to `main/master` build/test and push image to Docker Hub.
- Secrets required: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.

