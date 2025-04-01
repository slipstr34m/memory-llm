from fastapi import FastAPI
from .routes import user_profile

app = FastAPI()

# Include routes
app.include_router(user_profile.router)

