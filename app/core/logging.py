import sys
from pathlib import Path
from loguru import logger

def setup_logging() -> None:
    """Configure logging settings"""
    Path("logs").mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        serialize=True,
    )
    logger.add(
        "logs/error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="ERROR",
        rotation="1 day",
        retention="7 days",
    )
