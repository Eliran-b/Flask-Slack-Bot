import os
import slack
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from pathlib import Path
from slack_sdk.web.client import WebClient
import tweepy as tw

#.env file path 
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

#slack vars
slack_bot_token = os.environ['SLACK_BOT_TOKEN']
slack_app_token = os.environ['SLACK_APP_TOKEN']
content_channel_id = os.environ['CONTENT_CHANNEL_ID']

#twitter vars
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

#configurations
app = App(token=slack_bot_token)
auth = tw.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)


#client config
client = slack.WebClient(token=slack_bot_token)

#scheduler for cron tasks
scheduler = BackgroundScheduler(daemon=True)

#start thread
scheduler.start()


#send msg with the current time
def send_time_msg():
    """Send a message with the corrent hour to slack bot channel""" 
    try:
        tz = pytz.timezone('Israel')
        msg = str(datetime.now(tz).hour)+":"+str(datetime.now(tz).minute)
        client.chat_postMessage(channel='#content', text=msg)
    except Exception as e:
        print("Error: "+ type(e).__name__+ "\nMessage: "+ str(e))
    else: 
        return msg


#create schedule bot message - run before first request
@app.command("/init_sched")
def init_scheduler(ack):
    """Initialize the scheduler thread""" 
    # Acknowledge command request
    ack()
    scheduler.add_job(send_time_msg, 'interval', minutes=60)
    client.chat_postMessage(channel='#content', text="Schedule Started")



#now command
@app.command("/now")
def now(ack):
    """Post to the slack bot the current hour"""
    # Acknowledge command request
    ack()
    try:
        message = send_time_msg()
    except Exception as e:
        return {"Error": type(e).__name__, "Message": str(e)}, 500
    else:    
        return {"message": message}, 200



#twitter pages names, programming languages and their sources
language_dict = {"python": {"sources": ["@PythonWeekly", "@realpython", "@fullstackpython"],
                            },
                "javascript": {"sources": ["@JavaScriptDaily"],
                            },
                "c#": {"sources": ["@CSharpStack"],
                        },
                "c++": {"sources": ["@lefticus"],
                        },
                }




#pull twits from #Python Weekly, #Real Python, #Full Stack Python, #JavaScript Daily, #C# StackOverflow, #Jason Turner (for C++)
@app.command("/new_content")
def now(ack, payload):
    """Call this method by type /new_content and The Programming language tweets you want
        Programming Languages: c++, javascript, python, c#
    """
    # Acknowledge command request
    ack()
    text=payload['text']
    #if the programming language doesn't exist in the pages options 
    if not text:
        client.chat_postMessage(channel='#content', text="Please add the command a message content in this format:\n /new_content your_programming_language\nYou can choose one of these programming languages:\nc++ | javascript | c# | python ")
    else:        
        try: 
            tz = pytz.timezone('Israel')
            now = datetime.now(tz)
            hour_back = now - timedelta(hours=1)
            
            #save all the tweets from all the sources to one list
            tweets = []
            for source in language_dict[text]["sources"]:
                temp_tweets = api.user_timeline(screen_name=source)
                for tweet in temp_tweets:
                    #grab only the tweets in the last hour 
                    if tweet.created_at < now and tweet.created_at > hour_back:
                        tweets.append(tweet)
                        client.chat_postMessage(channel='#content', text=tweet.text)
            
            #if there is no tweets to post
            if tweets == []:
                client.chat_postMessage(channel='#content', text="There is no new tweets in {} sources".format(text))


        except Exception as e:
            return {"Error": type(e).__name__, "Message": str(e)}, 500
        else:
            return {"message": "Tweets Pulled Successfully"}, 200

    

#last tweet id - to make sure no tweet will be posted more than once
last_tweet = {"id": ""}


@app.command("/new_tweet")
def now(ack):
    """Check for new tweets and post them"""
    # Acknowledge command request
    ack()
    try:
        tweets=[]
        temp_tweets = api.user_timeline()
        for tweet in temp_tweets:
            #if we have reached the last tweet we have posted - break
            if tweet.id == last_tweet["id"]:
                break
            else:
                tweets.append(tweet)
                client.chat_postMessage(channel='#content', text=tweet.text)
        
        #if there is no new tweets to post       
        if tweets == []:
            client.chat_postMessage(channel='#content', text="There is no new tweets to post")
        else:      
            #update the last tweet sent
            last_tweet['id'] = tweets[0].id

    except Exception as e:
            return {"Error": type(e).__name__, "Message": str(e)}, 500
    else:
        return {"message": "Tweets Pulled Successfully"}, 200

 
    


#send /tweet and after it what you want to say
@app.command("/tweet")
def tweet(ack, payload):
    """Call this method by type /tweet and The message content you wish to post"""
    # Acknowledge command request
    ack()
    text=payload['text']
    if not text:
        client.chat_postMessage(channel='#content', text="Please add the command a message content in this format:\n /tweet your_message_content")
    else:
        #post tweet
        tweet = api.update_status(status=text)
        #update the last tweet sent
        last_tweet['id'] = tweet.id
      




if __name__ == "__main__":

    SocketModeHandler(app, slack_app_token).start()



