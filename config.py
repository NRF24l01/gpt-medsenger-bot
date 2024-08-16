import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv('PORT'))
HOST = os.getenv('HOST')
APP_KEY = os.getenv('APP_KEY')
MAIN_HOST = os.getenv('MAIN_HOST')

# Ai ai ai ai ai ai
AITYPE = int(os.getenv('AITYPE'))  # 1 - YaGPT, 2 - ChatGPT

# YAGPT
DIR_ID = os.getenv('DIR_ID')
API_KEY = os.getenv('API_KEY')

# ChatGPT
CHATGPT_MODEL = os.getenv('CHATGPT_MODEL')
CHATGPT_BASIC = os.getenv('CHATGPT_BASIC')
CHATGPT_HOST = os.getenv('CHATGPT_HOST')
CHATGPT_KEY = os.getenv('CHATGPT_KEY')

# Database
DB_LOGIN = os.getenv('DB_LOGIN')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_DATABASE = os.getenv('DB_DATABASE')


MAX_SESSION_TIME = int(os.getenv('MAX_SESSION_TIME'))
MAX_DOCTOR_TIME = int(os.getenv("MAX_DOCTOR_TIME"))
REDIS_HOST = os.getenv('REDIS_HOST')
