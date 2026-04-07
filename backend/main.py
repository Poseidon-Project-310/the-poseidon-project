from fastapi import FastAPI
from backend.routes import restaurant_router, search_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="The Poseidon Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(restaurant_router.router)
app.include_router(search_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to The Poseidon Project"}

@app.get("/health")
def health():
    return {"status": "ok"}
