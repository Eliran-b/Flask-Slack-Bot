import json
from db import db
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from models.message_box import MessageBox, messages_box_to_json
from resources.errors import abort_all_msg, abort_msg, abort_post_msg
from models.message import Message
from flask import request
from resources.utils import create_msg


class MessageRes(Resource):
    #parse request obj
    parser = reqparse.RequestParser() 
    parser.add_argument("receivers_username",
                        type=str,
                        help='Username of the receivers',
                        required=True
                       )
    parser.add_argument("message_body",
                        type=str,
                        help='Message body',
                        required=True
                       )
    parser.add_argument("message_subject",
                        type=str,
                        help='Message subject',
                        required=True
                       )
    
    @jwt_required()                   
    def post(self):
        """Create a new message"""
        #raise error if the username of one or all the receivers doesn't exist
        try:
            request_data = MessageRes.parser.parse_args()
            receivers_names = request.json["receivers_username"]
            del request_data["receivers_username"]
            msg_obj = create_msg(receivers_names, request_data)
        except:
            return abort_post_msg()
        else:
            return msg_obj.to_json(), 201


    @jwt_required()                   
    def get(self):
        """Get a message by an ID"""
        #make sure the data received in json format and contains the proper data
        try:
            msg_id = request.json["message_id"]
            msg_obj = Message.query.filter_by(id=msg_id).first()
            msg_box_obj = MessageBox.query.filter_by(message_id=msg_obj.id, user_id=current_user.id).first()
            #make the message read to True
            msg_box_obj.read = True
            db.session.commit()
        except:
            return abort_msg()
        else: 
            return msg_box_obj.to_json(), 201
        

    @jwt_required()                   
    def delete(self):
        """Delete a message from a sender and or receiver by its ID"""
        #make sure the data received in json format and contains the proper data
        try:
            msg_id = request.json['message_id']
            msg_obj = Message.query.filter_by(id=msg_id).first()
            msg_to_remove = MessageBox.query.filter_by(message_id=msg_obj.id, user_id=current_user.id).first()
            db.session.delete(msg_to_remove)
            db.session.commit()
        except:
            return abort_msg()
        else:
            return msg_obj.to_json(), 201



class MessageCollection(Resource):
    """Get all read and or unread messages for the logged in user"""
    @jwt_required()                   
    def get(self):
        #make sure the data received in json format and contains the proper data
        try:
            unread = request.json["unread"]
            #convert string to boolean
            bool_unread = json.loads(unread.lower())
            #if the user requested to get only the unread messages
            if bool_unread:
                msgs_box_obj = MessageBox.query.filter_by(user_id=current_user.id, read=False).all() 
            else:
                msgs_box_obj = MessageBox.query.filter_by(user_id=current_user.id).all() 
            #make the message read to True
            for msg_obj in msgs_box_obj:
                if msg_obj and not msg_obj.read:
                    msg_obj.read = True
                    db.session.commit()
        except:
                return abort_all_msg()        
        else:
            return messages_box_to_json(msgs_box_obj), 201
