from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import json

import os
from dotenv import load_dotenv
load_dotenv('.env')

from src.models import load_data
from src.bot import Bot, process_message

# === GLOBAL OBJECTS ===
client = MongoClient(os.environ.get('MONGODB_URI'))
db = client.streak
bot = Bot(token=os.environ['TELEGRAM_TOKEN'])
templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
  return templates.TemplateResponse(
    "index.html", {
      "participants": load_data(db.submissions.find()),
      "request": request,
    }
  )


@app.post("/hook")
async def hook(request: Request):
  process_message(bot, db, json.loads(await request.body()))
  return "OK"
