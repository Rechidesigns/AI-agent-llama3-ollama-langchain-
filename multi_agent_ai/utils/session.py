from uuid import UUID, uuid4
from fastapi import Request, Response

def _ensure_uuid(value: str | None) -> str | None:
    """Return a valid UUID string if possible, otherwise None."""
    if not value:
        return None
    try:
        return str(UUID(value))
    except Exception:
        return None

def get_or_create_session_id(
    request: Request,
    response: Response,
    cookie_max_age_seconds: int = 7 * 24 * 3600
) -> str:
    """
    Retrieves a UUID session ID from:
      1. X-Session-Id header
      2. session_id cookie
    If none exists, generates one and sets it in a cookie.
    """
    # Header first (for API/mobile clients)
    sid = _ensure_uuid(request.headers.get("X-Session-Id"))

    # Then cookie (for browsers)
    if not sid:
        sid = _ensure_uuid(request.cookies.get("session_id"))

    # Generate fresh one if needed
    if not sid:
        sid = str(uuid4())
        response.set_cookie(
            key="session_id",
            value=sid,
            max_age=cookie_max_age_seconds,
            httponly=True,
            samesite="lax",
            secure=False,  # True if HTTPS
        )
    return sid

