from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RouteNotFoundMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)  # Initialize the middleware with the app

    async def dispatch(self, request: Request, call_next):
        # Check if the route exists in the app's routing table
        route_exists = any(route.path == request.url.path for route in request.app.router.routes)

        # Check if the request path starts with '/static'
        if request.url.path.startswith('/static'):
            # Allow static file requests to go through
            response = await call_next(request)
            return response
        
        if not route_exists:
            # Log invalid route access if desired
            request.app.logger.warning(f"Invalid route accessed: {request.url.path}")

            # Return a custom response for undefined routes
            return JSONResponse(
                content={"detail": "Route not found"},
                status_code=404
            )

        # Proceed with the request if the route exists
        response = await call_next(request)
        return response
