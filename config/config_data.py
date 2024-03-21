from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_id: int
    crypto_address: str


@dataclass
class DataBase:
    url: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DataBase


def load_config(path: str):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_id=env('ADMIN_ID'),
            crypto_address=env('ADDRESS')
        ),
        db=DataBase(
            url=env('SQLALCHEMY_URL')
        )
    )