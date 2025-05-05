import uvicorn
from fastapi import FastAPI
from yet_another_todo_backend.resources import Entry, EntryManager
from fastapi.middleware.cors import CORSMiddleware
from yet_another_todo_backend.config import settings

app = FastAPI()


origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def hello_world():
    return {'hello': 'world'}


@app.get("/api/entries/")
async def get_entries():
    entry_manager = EntryManager(settings.data_folder)
    entry_manager.load()

    result = []
    for entry in entry_manager.entries:
        result.append(entry.json())

    return result


@app.post("/api/save_entries/")
async def save_entries(data: list[dict]):
    entry_manager = EntryManager(settings.data_folder)
    entry_manager.load()

    for entry in data:
        entry_manager.entries.append(Entry.from_json(entry))

    entry_manager.save()
    return {'statis': 'success'}


@app.get('/api/get_data_folder/')
async def get_data_folder():
    return {'folder': settings.data_folder}


if __name__ == "__main__":
    uvicorn.run("yet_another_todo_backend.app:app", host="0.0.0.0", port=8000, reload=True)
