from configs.locales import *
from configs.keyboards import *
from services.database import *
from utils.logger import *

from aiogram.utils.keyboard import *
from aiogram.filters import *
from aiogram.enums import *
from aiogram.types import *
from collections import *
from functools import *
from datetime import *
from aiogram import *
import requests
import asyncio

TOKEN = "TOKEN" #Rename to your actual token
MODEL_NAME = "MODEL_NAME" #Rename to a model listed in models.md or another model you know

MAX_HISTORY_LENGTH = 10
MEMORY_DURATION = 3600

user_command = {}

def texting(response, current_page, user):
    return f"<b>{user.full_name}</b>: {response[current_page][0]}\n\n<b>AI</b>: {response[current_page][1]}"