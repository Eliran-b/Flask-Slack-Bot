from logging import StreamHandler
import os
import slack
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from pathlib import Path
from slack_sdk.web.client import WebClient
import tweepy as tw
import pandas as pd


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

#slack vars
slack_bot_token = os.environ['SLACK_BOT_TOKEN']
slack_app_token = os.environ['SLACK_APP_TOKEN']
content_channel_id = os.environ['CONTENT_CHANNEL_ID']

#twitter vars
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET']
callback_uri = os.environ['CALLBACK_URI']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

app = App(token=slack_bot_token)
auth = tw.OAuthHandler(consumer_key, consumer_secret, callback_uri)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

# Get the User object for twitter...
user = api.get_user(screen_name='twitter')



#client config
client = slack.WebClient(token=slack_bot_token)

scheduler = BackgroundScheduler(daemon=True)


#start thread
scheduler.start()





#send msg with the current time
def send_time_msg(): 
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


#twitter pages names and programming languages
pages_dict = {"python": ["Python Weekly", "Real Python", "Full Stack Python"],
                "javascript": ["JavaScript Daily"],
                "c#": ["C# StackOverflow"],
                "c++": ["Jason Turner"]
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
        pass
    #if there is no tweets in history or the last tweet is more than one hour back:
    #    pull all twits from the last hour
    #if the last twit is less than one hour back
    #    pull all the twits until that last twit time
    #message = twits
    #args = programming language
    #client.chat_postMessage(channel='#content', text=message, args)
    


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
        api.update_status(status=text)





if __name__ == "__main__":

    SocketModeHandler(app, slack_app_token).start()



#from flask import Flask, request
#from flask_restful import Api, Resource
#from slackeventsapi import SlackEventAdapter



'''
app = Flask(__name__)

api = Api(app)

#client config
slack_token = str(subprocess.getstatusoutput(f'heroku config:get SLACK_BOT_TOKEN')[1])
client = slack.WebClient(token=slack_token)


scheduler = BackgroundScheduler(daemon=True)


#start thread
scheduler.start()

#send msg with the current time
def send_time_msg(): 
    try:
        tz = pytz.timezone('Israel')
        msg = str(datetime.now(tz).hour)+":"+str(datetime.now(tz).minute)
        client.chat_postMessage(channel='#content', text=msg)
    except Exception as e:
        print("Error: "+ type(e).__name__+ "\nMessage: "+ str(e))
    else: 
        return msg


#create schedule bot message
@app.before_first_request
def init_scheduler():
    scheduler.add_job(send_time_msg, 'interval', minutes=60)


#BOT_ID = client.api_call("auth.test")['user_id']
#create event == command sent by the user
#slack_signing_secret = str(subprocess.getstatusoutput(f'heroku config:get SIGNING_SECRET')[1])
#slack_event_adapter = SlackEventAdapter(slack_signing_secret, '/slack/events', app)

#now command
class Now(Resource):
    def post(self):
        try:
            message = send_time_msg()
        except Exception as e:
            return {"Error": type(e).__name__, "Message": str(e)}, 500
        else:    
            return {"message": message}, 200


api.add_resource(Now, "/now")

'''

'''
@slack_event_adapter.on('new-content')
def new_content(): 
    algorithm:
    if there is no tweets in history or the last tweet is more than one hour back:
        pull all twits from the last hour
    else #if the last twit is less than one hour back
        pull all the twits until that last twit time
    message = twits
    args = programming language
    client.chat_postMessage(channel='#content', text=message, args)
'''

'''
get all twits to the bot page

'''


'''
post new twits to the bot - make sure every twit post once
'''


'''
tweet command - post a new tweet
'''



#if __name__ == '__main__':
#    app.run()
    #app.run(debug=True)  


 