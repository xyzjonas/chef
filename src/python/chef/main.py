import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger
from starlette.staticfiles import StaticFiles

from chef.api import api_router
from chef.settings import settings


app = FastAPI()
app.include_router(api_router)

# for router in chef.api.routers:
#     app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serve():
    if settings.log_file:
        logger.add(settings.log_file, level=settings.log_level)

    if settings.serve_frontend:
        app.mount("/images", StaticFiles(directory=settings.images_folder))
        app.mount("/", StaticFiles(directory=settings.serve_frontend_path, html=True), name="static")

    options = "\n".join([f"{k.upper()}: '{v}'" for k, v in settings])
    logger.info(f"""

███████╗██╗  ██╗███████╗███████╗
██╔════╝██║  ██║██╔════╝██╔════╝
██║     ███████║█████╗  █████╗  
██║     ██╔══██║██╔══╝  ██╔══╝  
║██████ ██║  ██║███████╗██║     
╚═════════╝  ╚═╝╚══════╝╚═╝
...started with following settings:

{options}
    """)

    uvicorn.run(app)


if __name__ == '__main__':
    serve()