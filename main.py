from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from config.database import engine
from entities.schemas import user,stock
from entities.models.stock import Stock as stock_model
import paho.mqtt.client as mqtt
import time
import json
from config.database import get_db
from config.environment import MQTT_HOST,MQTT_PORT,MQTT_TOPIC
from repositories.stock_repo import create
from repositories.user_repo import check_pending

from routers.root import router

user.Base.metadata.create_all(engine)
stock.Base.metadata.create_all(engine)

db:Session = get_db

async def on_message(client, userdata, message):
    stock = json.loads(message.payload.decode("utf-8"))
    await create(stock_model(**stock),db)
    await check_pending(stock_model(**stock),db)

client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()
client.subscribe(MQTT_TOPIC)
client.on_message = on_message
time.sleep(15)
client.loop_end()

def get_application() -> FastAPI:
    application = FastAPI(title="ThndrTask", debug="DEBUG", version="0.0.0")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router, prefix="/api")

    return application

app = get_application()