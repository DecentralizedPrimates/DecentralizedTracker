import uvicorn as uvicorn
from fastapi import FastAPI

# For interacting with the network local client API should contain the following endpoints:
#
# MainDefaultSreen to display files by default on main screen. (GET)
# FileSearch to find a file by name and other parameters (GET)
# Settings (POST)
# Upload (POST)
# AddCategorie (POST)
# Download (GET)

app = FastAPI(
    title="DecetralizedTracker API",
    description="Local client API for interacting with the network.",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "MainDefaultSreen",
            "description": "Display files by default on main screen.",
        },
        {
            "name": "FileSearch",
            "description": "Find a file by name and other parameters.",
        },
        {
            "name": "Settings",
            "description": "",
        },
        {
            "name": "Upload",
            "description": "",
        },
        {
            "name": "AddCategorie",
            "description": "",
        },
        {
            "name": "Download",
            "description": "",
        },
    ],
)


@app.get("/", tags=["MainDefaultSreen"])
async def main_default_screen():
    return {""}


@app.get("/file_search", tags=["FileSearch"])
async def file_search():
    return {""}


@app.get("/settings", tags=["Settings"])
async def settings():
    return {""}


@app.post("/upload", tags=["Upload"])
async def upload():
    return {""}


@app.post("/add_categorie", tags=["AddCategorie"])
async def add_categorie():
    return {""}


@app.get("/download", tags=["Download"])
async def download():
    return {""}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload="True", log_level="info")
