from db import db


class MessageBox(db.Model):
    __tablename__ = 'messages_box'
    index = db.Column(
        db.Integer(), primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column('user_id', db.Integer(),
                            db.ForeignKey('users.id'))
    message_id = db.Column('message_id', db.Integer(),
                           db.ForeignKey('messages.id'))
    read = db.Column(db.Boolean(), default=False)
    receiver = db.Column(db.Boolean(), default=False)
    sender = db.Column(db.Boolean(), default=False)


    def __repr__(self):
        return '<MessageBox {}>'.format(self.index)


    def to_json(self):
        message_box_dict = {"message_box_index": self.index,
                        "user_id": self.user_id,
                        "message_id": self.message_id,
                        "read": self.read,
                        "receiver": self.receiver,
                        "sender": self.sender
                        }
        return message_box_dict


def messages_box_to_json(messages_box_obj_list):
    """return a json of all the messages in the list"""
    messages_box_dict={}
    i=0
    for message_box_obj in messages_box_obj_list:
        messages_box_dict[i] = message_box_obj.to_json()
        i+=1

    return messages_box_dict
