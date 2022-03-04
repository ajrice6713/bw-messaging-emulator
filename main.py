import uvicorn
from typing import Optional
from fastapi import FastAPI, Request, Response

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("2/minute")
def status_check(request: Request):
    """
    Test endpoint to ensure the server is running
    :param request:
    :return:
    """
    return "Hello World"


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, debug=True, reload=True)