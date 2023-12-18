import datetime
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import config_log_path
from model import models
from model.database import get_db_engine
from api import user, audio
import logging
logger = logging.getLogger(__name__)

# Set API
app = FastAPI()
origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# api related to user
app.include_router(user.router, tags=["User"], prefix="/api/user")
# api related to files
app.include_router(audio.router, tags=['Audio'], prefix="/api/audio")


# Set DB
db_engine = get_db_engine()
models.Base.metadata.create_all(bind=db_engine.engine)

# Set Log

# set log config
os.makedirs(config_log_path, exist_ok=True)
logger = logging.getLogger(__name__)
logging.basicConfig(filename=os.path.join(config_log_path, 'backend.log'),
                    level=logging.INFO,
                    format='%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s: %(message)s'
                    )
# show log on screen
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s: %(message)s')
console.setFormatter(console_format)
logging.getLogger().addHandler(console)


# Health Check
@app.get("/ping")
async def ping():
    logger.info(f"pinging the server")
    return {"message": f"pong! {datetime.datetime.now()}"}
