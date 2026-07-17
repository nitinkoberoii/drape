# AI service

This FastAPI service is reserved for stateless fashion inference in later
phases. During Phase 0 it exposes `GET /health` only, so infrastructure can
verify connectivity without downloading or initializing ML models.

Run locally after creating a virtual environment and installing requirements:

```sh
python main.py
```
