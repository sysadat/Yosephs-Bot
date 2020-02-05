import time
import tweepy

from keys import *

print("Hello! This is my twitter bot :)")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

fileName = "lastSeenID.txt"

def retrieveLastSeenID(fileName):
    fRead = open(fileName, "r")
    lastSeenID = int(fRead.read().strip())
    fRead.close()
    return lastSeenID

def storeLastSeenID(lastSeenID, fileName):
    fWrite = open(fileName, "w")
    fWrite.write(str(lastSeenID))
    fWrite.close()
    return

def replyToTweets():
    print("Retrieving and replying to tweets...")
    lastSeenID = retrieveLastSeenID(fileName)
    mentions = api.mentions_timeline(
                        lastSeenID,
                        tweet_mode = "extended")
    for mention in reversed(mentions):
        print(str(mention.id) + " - " + mention.full_text)
        lastSeenID = mention.id
        storeLastSeenID(lastSeenID, fileName)
        if "#hello" in mention.full_text.lower():
            print("Found #hello!")
            print("Responding back...")
            api.update_status("@" + mention.user.screen_name +
                    "#hello How are you?", mention.id)

while True:
    replyToTweets()
    time.sleep(20)
