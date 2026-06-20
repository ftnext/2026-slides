# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi>=0.138.0",
#     "uvicorn>=0.49.0",
# ]
# ///
from fastapi import FastAPI

app = FastAPI()
app.frontend("/", directory="build/revealjs")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
