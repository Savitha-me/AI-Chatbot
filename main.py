from fastapi import FastAPI
from database.postgres import Base, engine
import database.models
from api.routes.chat import router as chat_router


Base.metadata.create_all(bind=engine)
app=FastAPI(title="Enterprise Document Intelligence")
app.include_router(chat_router)