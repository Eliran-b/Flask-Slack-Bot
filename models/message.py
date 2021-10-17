from datetime import datetime
from db import db
from models.message_box import MessageBox




class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    #owner of the message
    sender_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    #receivers of the message
    #M:1 Relationship between message to receiver 
    message_boxes = db.relationship(
        'MessageBox', backref="messages", lazy='select')
    
    #the content of the message
    body = db.Column(db.Text)
    subject = db.Column(db.String(50))
    #creation date
    date = db.Column(db.Date(), unique=False, nullable=False)
    
    def __init__(self, message_body, message_subject):
        self.body = message_body
        self.subject = message_subject
        self.date = datetime.now()
      

    def __repr__(self):
        return '<Message {}>'.format(self.id)


    def to_json(self):
        from models.user import users_to_json
        dict_msg = {"message_id": self.id,
                    "sender_id": self.sender_id,
                    "receivers": users_to_json(self.users_received),
                    "body": self.body,
                    "subject": self.subject,
                    "date": str(self.date)                    
                    }
                    
        return dict_msg

        

        
