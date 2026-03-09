import time


def retry(fn, retries=3, delay=1):
    """Retry a function with exponential backoff."""
    last_error = None
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(delay * (2 ** attempt))

    raise last_error
