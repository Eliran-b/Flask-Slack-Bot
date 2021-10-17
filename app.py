from flask import Flask
from flask_restful import Api
from db import db
from security import bcrypt
import subprocess
import slack
from datetime import datetime
import pytz
from slackeventsapi import SlackEventAdapter


app = Flask(__name__)

#get the secret key and the uri from the heroku config var
secret_key = str(subprocess.getstatusoutput(f'heroku config:get SECRET_KEY')[1])
app.config['SECRET_KEY'] = secret_key
db_uri = str(subprocess.getstatusoutput(f'heroku config:get DATABASE_URL')[1])
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

db.init_app(app)
bcrypt.init_app(app)

#client config
#get the token from the heroku config var
token = str(subprocess.getstatusoutput(f'heroku config:get SLACK_TOKEN')[1])
client = slack.WebClient(token=token)
#time zone
tz = pytz.timezone('Israel')
#post message
#get the secret key from heroku config vars
'''
signing_secret_key = str(subprocess.getstatusoutput(f'heroku config:get SLACK_SIGNING_SECRET')[1])
slack_event_adapter = SlackEventAdapter(signing_secret_key, 'slack/events', app)
client.chat_postMessage(channel='#content', text=str(datetime.now(tz).time()))
'''





if __name__ == '__main__':
    #app.run()
    app.run(debug=True)  


