from fastapi import FastAPI
from database.postgres import Base, engine
import database.models
from api.routes.chat import router as chat_router
from api.routes.auth import router as auth_router
from api.routes.summary import router as summary_router

Base.metadata.create_all(bind=engine)
app=FastAPI(title="Enterprise Document Intelligence")
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(summary_router)