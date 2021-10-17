from models.user import User
from models.message_box import MessageBox
from models.message import Message
from flask_jwt_extended import current_user
from db import db

def create_msg(users_names, request_data):
    #create message object
    msg_obj = Message(**request_data)  
    db.session.add(msg_obj)

    #current user msg box object
    msg_box_obj = MessageBox()
    msg_box_obj.read = True
    msg_box_obj.sender = True
    db.session.add(msg_box_obj)
    #create message_box relationships
    current_user.messages_box.append(msg_box_obj)
    current_user.messages_sent.append(msg_obj)
    #create message relationship
    msg_obj.message_boxes.append(msg_box_obj)
    db.session.commit()

    #the receivers objects creation
    for user_name in users_names:
        user_obj = User.query.filter_by(username=user_name).first()
        #create message_box object
        msg_box_obj = MessageBox()
        msg_box_obj.receiver = True
        db.session.add(msg_box_obj)
        #create user relationship with message and message box objects
        user_obj.messages_box.append(msg_box_obj)
        user_obj.messages_received.append(msg_obj)
        #create message box relationship
        msg_obj.message_boxes.append(msg_box_obj)
        db.session.commit()

    return msg_obj