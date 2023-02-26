from aiohttp.web import run_app
from app.chat.app import setup_app

if __name__ == "__main__":
    run_app(setup_app(), host='127.0.0.1')
