# main.py

from fastapi import FastAPI
from app.api.main import main_router

app = FastAPI()

# Include the main_router
app.include_router(main_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

