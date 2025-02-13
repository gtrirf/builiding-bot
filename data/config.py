from environs import Env
import os
import time

env = Env()
env.read_env()


os.environ['TZ'] = 'Asia/Tashkent'


BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")


