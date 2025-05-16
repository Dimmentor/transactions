from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import users, transactions, categories


app = FastAPI(title="bboom")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(categories.router)


@app.get("/")
async def root():
    return {"message": "Проект bboom запущен"}