from flask import Flask
from flask_restful import Api
import slack
from datetime import datetime
import pytz
from slackeventsapi import SlackEventAdapter
import subprocess

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

#client config
slack_token = str(subprocess.getstatusoutput(f'heroku config:get SLACK_TOKEN')[1])
client = slack.WebClient(token=slack_token)
#time zone
tz = pytz.timezone('Israel')
#post message
slack_signing_secret = str(subprocess.getstatusoutput(f'heroku config:get SIGNING_SECRET')[1])
slack_event_adapter = SlackEventAdapter(slack_signing_secret, '/slack/events', app)
client.chat_postMessage(channel='#content', text=str(datetime.now(tz).time()))





if __name__ == '__main__':
    #app.run()
    app.run(debug=True)  


