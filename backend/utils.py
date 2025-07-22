import logging
import os

# Constants
LOGFILE = "app.log"
UPLOAD_DIR = "data"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGFILE),
        logging.StreamHandler()
    ],
)

def ensure_upload_dir(path: str = UPLOAD_DIR):
    """Ensure the upload/data directory exists."""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"✔ Upload/data folder ensured at: '{path}'")
    except Exception as e:
        logging.error(f"❌ Failed to create upload directory '{path}': {e}")
        raise
