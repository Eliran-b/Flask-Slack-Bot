from flask_jwt_extended.utils import create_access_token
from flask_restful import Resource, reqparse
from models.user import User
from db import db
from resources.errors import abort_create_user, abort_login_user

class UserRegister(Resource):
    """Register new user"""
    #parse request obj
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        help='Choose username with alphabetical charecters only',
                        required=True
                        )
    parser.add_argument("password",
                        type=str,
                        help='Choose password to register',
                        required=True
                       )
    def post(self):
        #make sure the data received in json format and contains the proper data
        try:
            request_data = UserRegister.parser.parse_args()
            username = request_data['username']
            password = request_data['password']
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity={"username": username})
        except:
            return abort_create_user()
        else:
            return {"access_token": access_token}, 200
    
    
class UserLogin(Resource):
    """Login to a user account"""
    #parse request obj
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        help='Account Username',
                        required=True
                        )
    parser.add_argument("password",
                        type=str,
                        help='Account Password',
                        required=True
                       )
    def post(self):
        #make sure the data received in json format and contains the proper data
        try:
            request_data = UserRegister.parser.parse_args()
            username = request_data['username']
            user = User.query.filter_by(username=username, active=True).first()
            access_token = create_access_token(identity={"username": user.username})
        except:
            return abort_login_user()
        else:
            return {"access_token": access_token}, 200

        

