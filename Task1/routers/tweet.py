from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from internal.token import manager
from database import db_session
from database.models import Tweet


router = APIRouter(
    prefix="/tweet",
    tags=["Tweet"],
    responses={404: {"description": "Not found"}},
)

class TweetPayload(BaseModel):
    """Tweet Payload for posting a tweet

    Args:
        BaseModel (_type_): pydantic
    """
    tweet: str

class TweetUpdatePayload(BaseModel):
    """Tweet Payload for updating a tweet

    Args:
        BaseModel (_type_): pydantic
    """
    tweet: str
    id: int

class TweetDeletePayload(BaseModel):
    """Tweet Payload for deleting a tweet

    Args:
        BaseModel (_type_): pydantic
    """
    id: int

class TweetLikeRetweetPayload(BaseModel):
    """Tweet Payload for liking and retweeting a tweet

    Args:
        BaseModel (_type_): pydantic
    """
    id: int


@router.get("/get-tweet", status_code=status.HTTP_200_OK) 
async def get_user_tweets(user=Depends(manager)):
    """This Route is used to get the user tweets and also the tweets which
       user has retweeted

    Args:
        user (LoginManager, optional): Login manger. Defaults to Depends(manager).

    Raises:
        HTTPException: 418 in case of exception

    Returns:
        dict: tweet list
    """
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
        raise HTTPException(
                status_code=418, detail="Exception occurred while fetching tweets"
            )


@router.post("/post-tweet", status_code=status.HTTP_201_CREATED)
async def post_tweet(data: TweetPayload, user=Depends(manager)):
    """This Route is used to post tweets.

    Args:
        user (LoginManager, optional): Login manger. Defaults to Depends(manager).

    Raises:
        HTTPException: 418 in case of exception

    Returns:
        str: Status
    """
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
    """This Route is used to update tweets

    Args:
        user (LoginManager, optional): Login manger. Defaults to Depends(manager).

    Raises:
        HTTPException: 418 in case of exception

    Returns:
        str: status
    """
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
    """This Route is used to delete user tweet

    Args:
        user (LoginManager, optional): Login manger. Defaults to Depends(manager).

    Raises:
        HTTPException: 418 in case of exception

    Returns:
        str: status
    """
    try:
        obj = db_session.query(Tweet).filter(Tweet.id == data.id).first()
        if obj:
            db_session.delete(obj)
            db_session.commit()
            return "Your tweet is deleted"
        else:
            return "Tweet not found"
    except Exception:
        db_session.rollback()
        raise HTTPException(
                status_code=418, detail="Exception occurred while deleting"
            )


@router.post("/like-tweet", status_code=status.HTTP_201_CREATED)
async def like_tweet(data: TweetLikeRetweetPayload, user=Depends(manager)):
    """This Route is used to like other tweets

    Args:
        user (LoginManager, optional): Login manger. Defaults to Depends(manager).

    Raises:
        HTTPException: 418 in case of exception

    Returns:
        str: status
    """
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
    """This Route is used to unlike tweets

    Args:
        user (LoginManager, optional): Login manger. Defaults to Depends(manager).

    Raises:
        HTTPException: 418 in case of exception

    Returns:
        str: status
    """
    try:
        obj = db_session.query(Tweet).filter(Tweet.id == data.id).first()
        if(obj):
            val = list(obj.likes)
            if(tuple(user)[3] in val): # checks if the user has liked the tweet or not
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
    """This Route is used to retweet a tweet.

    Args:
        user (LoginManager, optional): Login manger. Defaults to Depends(manager).

    Raises:
        HTTPException: 418 in case of exception

    Returns:
        dict: tweet list
    """
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
