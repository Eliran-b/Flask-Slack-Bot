from flask_restful import abort

def abort_msg():
        """ Abort if message ID does not found """
        abort(404, message="Message id is not valid or does not exist in user database")

def abort_all_msg():
        """ Abort no messages found """
        abort(404, message="No messages found in user database")

def abort_post_msg():
        """ Abort if could not create a message object """
        abort(500, message="Internal error occurred while trying to create a new message")

def abort_create_user():
        """ Abort if could not create a user object """
        abort(500, message="Internal error occurred while trying to create a new user. The username may already exist in the database")

def abort_login_user():
        """ Abort if could not login with to the user account """
        abort(500, message="Internal error occurred while trying to connect to the account")

