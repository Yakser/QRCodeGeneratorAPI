from tokens_storage import TokensStorage
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
from uvicorn import Server, Config
from fastapi import BackgroundTasks, FastAPI
from fastapi.staticfiles import StaticFiles

# from api.constants import BASE_URL

BASE_URL = '/api'
FILE_PATH = 'static/qr-code-'
PORT = os.environ.get('PORT')


app = FastAPI()

origins = [
    "https://react-qrcode-generator.herokuapp.com",
    "http://react-qrcode-generator.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

loop = asyncio.get_event_loop()

app.mount("/static", StaticFiles(directory='./static'), name="static")
storage = TokensStorage()


async def clean_storage(token):
    await storage.find_and_delete(token)


@app.get(BASE_URL + '/generate')
async def generate_page(background_tasks: BackgroundTasks, text: str):
    try:
        token = storage.generate_qrcode(text)
        background_tasks.add_task(clean_storage, token)
        return {'message': 'ok', 'token': token}
    except Exception as e:
        print(e)
        return {'message': 'error'}


# config = Config(app=app, host='0.0.0.0', port=PORT, loop=loop)
# server = Server(config)
# loop.run_until_complete(server.serve())

# if __name__ == '__main__':
#    uvicorn.run('app:app', host="0.0.0.0", port=5000)
