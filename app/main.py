from fastapi import FastAPI
from database import get_db, Base, engine
import uvicorn

app = FastAPI()


# Инициализация базы данных при старте
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
