from fastapi import FastAPI
from database.postgres import Base, engine
import database.models
from api.routes.chat import router as chat_router
from api.routes.auth import router as auth_router
from api.routes.summary import router as summary_router
from api.routes.documents import router as documents_router

#create databse tables
Base.metadata.create_all(bind=engine)

#create FastAPI application
app=FastAPI(
    title="Enterprise Document Intelligence"
)

#Register APi routers
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(summary_router)
app.include_router(documents_router)