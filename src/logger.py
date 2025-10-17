from loguru import logger
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "bot.log"

rotation_size = 5 * 1024 * 1024  # 5 MB
retention_days = 7  # 7 days
compression = "zip"  # Compress old logs to save space

logger.remove()  # Remove the default logger to avoid duplicate logs
logger.add(sys.stdout, level="INFO")  # Log to console
logger.add(
    str(LOG_FILE),
    level="DEBUG",
    rotation=rotation_size,
    retention=retention_days,
    compression=compression,
    backtrace=True,
    diagnose=True,
    enqueue=True,  # Ensure thread safety
    
)

def get_logger():
    return logger