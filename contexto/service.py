import os
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from contexto.config import ROOT_DIR
from contexto.guess import Finder

app = FastAPI()
finder = Finder()


class Guess(BaseModel):
    word: str
    order: int


class Guesses(BaseModel):
    guesses: List[Guess]


@app.post("/api/predict")
async def predict(query: Guesses):
    guesses = [
        (guess.word, guess.order)
        for guess in query.guesses
    ]

    return {
        "result": finder.guess_next(guesses, word_to_distances=finder.get_word_to_distances(guesses))
    }


app.mount("/", StaticFiles(directory=os.path.join(ROOT_DIR, 'frontend', 'dist', 'spa'), html=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
