import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    data_folder: str = '/tmp/'
    frontend_url: str = os.getenv('FRONTEND_URL')


settings = Settings()
