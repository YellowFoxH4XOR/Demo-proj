"""
    Main Class which created Api object
"""

from unicodedata import name
from fastapi import Depends, FastAPI
from internal import token
from routers import user, tweet

app = FastAPI(title="bitter")

app.include_router(user.router) # user addition and status
app.include_router(token.router) # Creation of token based on user details
app.include_router(tweet.router) # Tweet functionality
