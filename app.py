from flask import Flask
import slack
from datetime import datetime
import pytz
from slackeventsapi import SlackEventAdapter
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

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



def send_msg(message): 
    client.chat_postMessage(channel='#content', text=message)


#client config
slack_token = str(subprocess.getstatusoutput(f'heroku config:get SLACK_TOKEN')[1])
client = slack.WebClient(token=slack_token)
#slack_signing_secret = str(subprocess.getstatusoutput(f'heroku config:get SIGNING_SECRET')[1])
#slack_event_adapter = SlackEventAdapter(slack_signing_secret, '/slack/events', app)






if __name__ == '__main__':
    #app.run()
    app.run(debug=True)  


 