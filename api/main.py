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

@app.get(path='/profile/{user}')
def get_profile(user: str):
    return {f"This is a profile page for - {user}"}

