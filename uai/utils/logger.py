import logging
import time

logger = logging.getLogger("uai")


def log_request(provider_name, prompt, duration, token_count=None):
    """Log an AI request with timing information."""
    msg = f"[{provider_name}] {duration:.2f}s"
    if token_count is not None:
        msg += f" | {token_count} tokens"
    logger.info(msg)
