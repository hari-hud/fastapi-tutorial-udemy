from fastapi import FastAPI

app = FastAPI()


@app.get(path='/')
def index():
    return 'Hello, World!'

@app.get(path='/movies')
def movies():
    return {
        "Movies": ['movie1', 'movie2']
    }


