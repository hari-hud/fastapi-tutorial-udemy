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

# Path Parameter: parameters passed in path
@app.get(path='/profile/{user}')
def get_profile(user: str):
    return {f"This is a profile page for - {user}"}

# Query Parameter: When parameter is passed in func but not in path
# to make query params optional we can set their values to None.
# /products?id=1&price=100
@app.get('/products')
def products(id: int = 1, price: str = None):
    return {f"Product with an Id: {id} and price: {price}"}

# Query + Path parameter
# /profile/{id}/comments?commentid=123
@app.get('/profile/{id}/comments')
def comments(id: int, commentid: int):
    return {f"Profile page for user Id: {id} and comment: {commentid}"}
