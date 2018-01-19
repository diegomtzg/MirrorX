
from speechManager import *
from audio_engine import *

class SelfiePoster: # (twitter_helpers.CozmoTweetStreamListener)
    def __init__(self, twitter_api):
        self.twitter_api = twitter_api
        self.owner_username = OWNER_TWITTER_USERNAME
        self.owner_name = OWNER_FACE_ENROLL_NAME

twitter_api, twitter_auth = twitter_helpers.init_twitter(twitter_keys)
selfiePost = SelfiePoster(twitter_api)

def do_takePicture(robot):
    # robot.camera.image_stream_enabled = True
    print("taking a picture...")
    pic_filename = "picture.png"
    # robot.say_text("Say cheese!").wait_for_completed()
    
    latest_image = robot.world.latest_image
    
    latest_image.raw_image.convert('L').save(pic_filename)
    print("picture saved as: " + pic_filename)

    # Ask: "Who do you want to tweet at?"

    tweetFilter = True
    usernameForTweet = recognizeSpeech("tweet")

    # Ask: "What will your caption be?"

    status_text = "@" + usernameForTweet + " " + recognizeSpeech("tweet")
    media_ids = twitter_helpers.upload_images(selfiePost.twitter_api, [latest_image.raw_image])
    posted_image = twitter_helpers.post_tweet(selfiePost.twitter_api, status_text, media_ids=media_ids)








