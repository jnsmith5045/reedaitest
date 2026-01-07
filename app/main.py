"""Minimal FastAPI application that serves a random number."""
from __future__ import annotations

import os
import random
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

DEFAULT_MIN = 0
DEFAULT_MAX = 1_000_000

app = FastAPI(title="Random Number API", version="0.1.0")


class RandomNumber(BaseModel):
    number: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/random", response_model=RandomNumber)
def get_random_number(min_value: Optional[int] = None, max_value: Optional[int] = None) -> RandomNumber:
    """Return a random number as JSON.

    Optional query parameters allow overriding the default bounds. They are clamped so
    ``min_value`` is always less than ``max_value``.
    """

    lower = DEFAULT_MIN if min_value is None else min_value
    upper = DEFAULT_MAX if max_value is None else max_value

    if lower >= upper:
        upper = lower + 1

    value = random.randint(lower, upper)
    return RandomNumber(number=value)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
