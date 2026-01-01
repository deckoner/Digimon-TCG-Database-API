from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi import Request


class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Prevent error caching (status >= 400)
        if response.status_code >= 400:
            return response

        path = request.url.path

        # Routes that should not be cached
        no_cache_prefixes = ["/decks", "/collections"]

        if any(path.startswith(prefix) for prefix in no_cache_prefixes):
            # We do not add cache header
            return response

        # Routes that can be cached
        if path.startswith("/aux/") or path.startswith("/cards/"):
            response.headers["Cache-Control"] = "public, max-age=3600"

        return response
