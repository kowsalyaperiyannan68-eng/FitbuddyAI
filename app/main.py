import sys
from pathlib import Path

# Make the project root importable so the ``app.*`` imports below work no matter
# how this file is launched: the VS Code "Run" button (python app/main.py),
# ``python -m app.main``, or ``python -m uvicorn app.main:app``.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import router

_STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description=(
        "AI-powered personalized fitness "
        "plan generator using Gemini."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(directory=str(_STATIC_DIR)),
    name="static",
)


app.include_router(router)


if __name__ == "__main__":

    import uvicorn

    # Pass the app object directly so it starts reliably regardless of the
    # working directory. For auto-reload during development, run instead:
    #   python -m uvicorn app.main:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
