from fastapi import Depends, FastAPI
from internal import token
from routers import user, tweet


app = FastAPI()

app.include_router(user.router)
app.include_router(token.router)
app.include_router(tweet.router)

