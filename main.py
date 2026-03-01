from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import connect_db, close_db
from auth_routes import router as auth_router
from user_routes import router as user_router


# ─── Lifespan (startup + shutdown) ────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()       # startup — connect to MongoDB
    yield
    await close_db()         # shutdown — close connection


# ─── App Init ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="AI Agent Platform",
    description="FastAPI backend with JWT auth and MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)


# ─── CORS ─────────────────────────────────────────────────────────────────────


app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:3000"],   # Next.js frontend
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ─── Routers ──────────────────────────────────────────────────────────────────

app.include_router(auth_router)
app.include_router(user_router)


# ─── Health Check ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "AI Agent Platform API is running 🚀"}