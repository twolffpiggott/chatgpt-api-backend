from app.api import chats, labels
from app.database import base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chats.router, prefix="/chats", tags=["chats"])
app.include_router(labels.router, prefix="/chats/{chat_id}/labels", tags=["labels"])


# Initialize database
@app.on_event("startup")
def startup_event():
    base.init_db()
