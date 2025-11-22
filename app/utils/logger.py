import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("banking_api")

def log_info(msg, user_id=None):
    prefix = f"[USER {user_id}] " if user_id else ""
    logger.info(f"✅ {prefix}{msg}")

def log_warning(msg, user_id=None):
    prefix = f"[USER {user_id}] " if user_id else ""
    logger.warning(f"⚠️ {prefix}{msg}")

def log_error(msg, user_id=None):
    prefix = f"[USER {user_id}] " if user_id else ""
    logger.error(f"❌ {prefix}{msg}")

def log_security(event, user_id=None):
    prefix = f"[USER {user_id}] " if user_id else ""
    logger.warning(f"🔒 SECURITY: {prefix}{event}")