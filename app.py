from flask import Flask
from flask_restful import Api
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import pytz
from slackeventsapi import SlackEventAdapter


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

#client config
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
#time zone
tz = pytz.timezone('Israel')
#post message
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], 'slack/events', app)
client.chat_postMessage(channel='#content', text=str(datetime.now(tz).time()))





if __name__ == '__main__':
    #app.run()
    app.run(debug=True)  


