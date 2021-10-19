from flask import Flask, request, Response
import slack
from slackeventsapi import SlackEventAdapter
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.exceptions import InternalServerError
from datetime import datetime
import pytz

app = Flask(__name__)

#client config
slack_token = str(subprocess.getstatusoutput(f'heroku config:get SLACK_TOKEN')[1])
client = slack.WebClient(token=slack_token)

scheduler = BackgroundScheduler(daemon=True)

#start thread
scheduler.start()

def send_time_msg(): 
    tz = pytz.timezone('Israel')
    msg = str(datetime.now(tz).hour)+":"+str(datetime.now(tz).minute)
    client.chat_postMessage(channel='#content', text=msg)

@app.before_first_request
def init_schedule(): 
    #create schedule email notification
    scheduler.add_job(send_time_msg, 'interval',minutes=60)

#create event == command sent by the user
#slack_signing_secret = str(subprocess.getstatusoutput(f'heroku config:get SIGNING_SECRET')[1])
#slack_event_adapter = SlackEventAdapter(slack_signing_secret, '/slack/events', app)

@app.route('/now', methods=['POST'])
def now(): 
    #channel_id = request.form.get('channel_id')
    tz = pytz.timezone('Israel')
    #msg = str(datetime.now(tz).hour)+":"+str(datetime.now(tz).minute)
    return Response(tz), 200
    
    '''
    try:
        send_time_msg()
    except InternalServerError as e:
        return {"message": "Internal server error occurred"}, 500
    else:
        return {}, 200
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
post new twits automatically to the bot - make sure every twit post once
'''


'''
tweet command - post a new tweet
'''



if __name__ == '__main__':
    app.run()
    #app.run(debug=True)  


 