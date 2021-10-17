from db import db
from security import bcrypt
from models.message import Message
from models.message_box import MessageBox

#association table in M:N relationship between user to messages received
user_received_msg = db.Table('user_received_msg',
    db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('messages_id', db.Integer(), db.ForeignKey('messages.id'))
)


class User(db.Model):   
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(30), unique=True, nullable=False) 
    password_hash = db.Column(db.String(60), unique=False, nullable=False)
    active = db.Column(db.Boolean(), unique=False, default=True)
    
    #M:1 Relationship between user to receiver (himself)
    messages_box = db.relationship(
        'MessageBox', backref='user', lazy='select')

    #M:1 Relationship between user to message that he sent
    messages_sent = db.relationship(
        'Message', backref="users_sent", lazy='select')

    #M:N Relationship between users to message that they received 
    messages_received = db.relationship(
        'Message', secondary=user_received_msg, backref="users_received", lazy='select')
    
  

    def __init__(self, username, password):
        self.username = username
        self.password = password

   
    def __repr__(self):
        return '<User {}>'.format(self.id)

    

    #getter
    @property 
    def password(self):
        return self.password
        
    #setter
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
   
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
 

    #return True if user is active
    def is_active(self):
        return self.active




    def to_json(self):
            user_dict = {"user_id": self.id,
                        "username": self.username,
                        "active": self.active,
                        }
            return user_dict

def users_to_json(users_obj_list):
    """return a json of all the users in the list"""
    users_obj_dict={}
    i=0
    for user_obj in users_obj_list:
        users_obj_dict[i] = user_obj.to_json()
        i+=1

    return users_obj_dict