from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from .routes import user_profile
from ipaddress import ip_address


app = FastAPI()

class BlockPublicIPMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        async def asgi(receive, send):
            client_ip = scope["client"][0]
            try:
                ip = ip_address(client_ip)
                if ip.is_global:
                    raise HTTPException(status_code=403, detail="Public IP access forbidden")
            except ValueError:
                pass  # Invalid IP address, continue processing
            return await self.app(scope, receive, send)
        
        try:
            await asgi(receive, send)
        except HTTPException as exc:
            response = JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
            await response(scope, receive, send)


# Include routes
app.include_router(user_profile.router)
app.add_middleware(BlockPublicIPMiddleware)
