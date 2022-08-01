import logging
import sys
import os
from datetime import timedelta
from typing import List
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

config = Config(".env", os.environ)

MQTT_HOST:str = config("MQTT_HOST", cast=str, default="172.18.0.2")
MQTT_PORT:int = config("MQTT_PORT", cast=int, default=1883)
MQTT_TOPIC:str = config("MQTT_TOPIC", cast=str, default="thndr-trading")

DATABASE_USERNAME:str = config("DATABASE_USERNAME", cast=str, default="")
DATABASE_PASSWORD:str = config("DATABASE_PASSWORD", cast=str, default="")
DATABASE_ENDPOINT:str = config("DATABASE_ENDPOINT", cast=str, default="database-1.cghw47lxnbct.us-east-1.rds.amazonaws.com")
DATABASE_PORT:str = config("DATABASE_PORT", cast=str, default="5432")
DATABASE_NAME:str = config("DATABASE_NAME", cast=str, default="thndr")