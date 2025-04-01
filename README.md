# Menstrunation Backend

## Python Environment

Im Terminal im Projektordner:

- python -m venv myenv (or python3 -m venv myenv)
(Sollte es nicht funktionieren, stelle sicher, dass dein System Python installiert hat)

- source myenv/bin/activate
- pip install -r requirements.txt


## Docker Environment

Im Terminal im Projektordner:

- docker compose up -d


## FastAPI development

Im Terminal im Projektordner:

- uvicorn main:app --reload