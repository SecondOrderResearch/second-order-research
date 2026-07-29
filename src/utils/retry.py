from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

def http_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.RequestException,)),
    )
