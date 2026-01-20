from environs import Env
from dataclasses import dataclass
import os

@dataclass
class Database:
    name: str
    user: str
    password: str
    host: str

@dataclass
class Config:
    db: Database

def load_config(path=None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        db=Database(
            name=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST')
        )
    )
