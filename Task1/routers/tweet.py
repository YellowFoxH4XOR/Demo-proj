from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from internal.token import manager
from database import db_session
from database.models import Tweet
import traceback


router = APIRouter(
    prefix="/tweet",
    tags=["Tweet"],
    responses={404: {"description": "Not found"}},
)

class TweetPayload(BaseModel):
    tweet: str

class TweetUpdatePayload(BaseModel):
    tweet: str
    id: int

class TweetDeletePayload(BaseModel):
    id: int

class TweetLikeRetweetPayload(BaseModel):
    id: int

@router.get("/get-tweet", status_code=status.HTTP_200_OK) 
async def get_user_tweets(user=Depends(manager)):
    try:
        user_id = tuple(user)[3]
        db_obj = db_session.query(Tweet).filter(Tweet.owner_id == user_id).all()
        db_obj_retweet = db_session.query(Tweet).all()
        self_tweet_list = []
        retweet_list = []
        if db_obj:
            for tweet in db_obj:
                response = {
                    'tweet': tweet.tweet,
                    'likes': len(tweet.likes),
                    'retweet_count': len(tweet.retweet)
                }
                self_tweet_list.append(response)
        if(db_obj_retweet):
            for item in db_obj_retweet:
                if(user_id in list(item.retweet)):
                    response = {
                        'tweet': item.tweet,
                        'likes': len(item.likes),
                        'retweet_count': len(item.retweet)
                    }
                    retweet_list.append(response)
        result = {"tweets": self_tweet_list, "retweets": retweet_list}
        return result
    except Exception:
        print(traceback.format_exc())
        raise HTTPException(
                status_code=418, detail="Exception occurred while fetching tweets"
            )


@router.post("/post-tweet", status_code=status.HTTP_201_CREATED)
async def post_tweet(data: TweetPayload, user=Depends(manager)):
    try:
        tweet_obj = Tweet(
            tweet = data.tweet,
            owner_id = tuple(user)[3]
        )
        db_session.add(tweet_obj)
        db_session.commit()
        return "Your tweet is active"
    except Exception:
        db_session.rollback()
        raise HTTPException(
                status_code=418, detail="Exception occurred while saving details"
            )

@router.put("/update-tweet", status_code=status.HTTP_201_CREATED)
async def update_tweet(data: TweetUpdatePayload, user=Depends(manager)):
    try:
        db_session.query(Tweet).filter(Tweet.id == data.id).update(
            {
                Tweet.tweet: data.tweet
            },
            synchronize_session=True
        )
        db_session.commit()
        return "Your tweet is updated"
    except Exception:
        db_session.rollback()
        raise HTTPException(
                status_code=418, detail="Exception occurred while updating"
            )

@router.delete("/delete-tweet", status_code=status.HTTP_202_ACCEPTED)
async def delete_tweet(data: TweetDeletePayload, user=Depends(manager)):
    try:
        db_session.query(Tweet).filter(Tweet.id == data.id).delete()
        db_session.commit()
        return "Your tweet is deleted"
    except Exception:
        db_session.rollback()
        raise HTTPException(
                status_code=418, detail="Exception occurred while deleting"
            )


@router.post("/like-tweet", status_code=status.HTTP_201_CREATED)
async def like_tweet(data: TweetLikeRetweetPayload, user=Depends(manager)):
    try:
        obj = db_session.query(Tweet).filter(Tweet.id == data.id).first()
        if(obj):
            val = list(obj.likes)
            val.append(tuple(user)[3])
            obj.likes = val
            db_session.commit()
            return "Liked"
        else:
            return "Tweet not Found"
    except Exception:
        db_session.rollback()
        raise HTTPException(
                status_code=418, detail="Exception occurred"
            )

@router.post("/unlike-tweet", status_code=status.HTTP_201_CREATED)
async def unlike_tweet(data: TweetLikeRetweetPayload, user=Depends(manager)):
    try:
        obj = db_session.query(Tweet).filter(Tweet.id == data.id).first()
        if(obj):
            val = list(obj.likes)
            if(tuple(user)[3] in val):
                val.remove(tuple(user)[3])
            else:
                return "You have not liked the tweet"
            obj.likes = val
            db_session.commit()
            return "UnLiked"
        else:
            return "Tweet not Found"
    except Exception:
        db_session.rollback()
        raise HTTPException(
                status_code=418, detail="Exception occurred"
            )


@router.post("/re-tweet", status_code=status.HTTP_201_CREATED)
async def re_tweet(data: TweetLikeRetweetPayload, user=Depends(manager)):
    try:
        obj = db_session.query(Tweet).filter(Tweet.id == data.id).first()
        if obj:
            val = list(obj.retweet)
            val.append(tuple(user)[3])
            obj.retweet = val
            db_session.commit()
            return "Retweeted"
        else:
            return "Tweet not Found"
    except Exception:
        db_session.rollback()
        raise HTTPException(
                status_code=418, detail="Exception occurred"
            )