import uvicorn
from pathlib import Path
from dotenv import load_dotenv
from app.config import get_settings

ROOT_DIR = Path(__file__).resolve().parent
ENV_FILE = ROOT_DIR / ".env"

load_dotenv(ENV_FILE, override=True)

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
        reload_includes=[
            "app/**/*.py",
            ".env"
        ],
        reload_excludes=["logs/**/*.log", "*.log"],
        log_level=settings.log_level.lower(),
    )
