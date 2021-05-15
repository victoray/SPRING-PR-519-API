import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from albums.router import album_router
from photos.router import photo_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"version": app.version}


app.include_router(photo_router)
app.include_router(album_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
