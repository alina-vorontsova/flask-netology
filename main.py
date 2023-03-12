
from flask import Flask, jsonify, request
from flask.views import MethodView 
from sqlalchemy.exc import IntegrityError

from db import Session 
from models import Advertisement, User
from errors import HttpError 
from schema import AdCreation, AdPatching, UserCreation, UserPatching
from tools import validate, get_ad, get_user, hash_password

app = Flask('ads_site')


@app.errorhandler(HttpError)
def error_handler(error: HttpError):

    response = jsonify({'status': 'error', 'description': error.description})
    response.status_code = error.status_code

    return response 


class AdView(MethodView):

    def get(self, ad_id: int):
        with Session() as session: 
            ad = get_ad(ad_id, session)
            return jsonify({'id': ad.id, 
                            'title': ad.title, 
                            'owner': ad.user_id, 
                            'creation_info': ad.created_at, 
                            'description': ad.description})
        
    def post(self):
        json_data = validate(request.json, AdCreation)
        with Session() as session:
            ad = Advertisement(**json_data)
            session.add(ad)
            session.commit()
            return jsonify({'id': ad.id, 
                            'title': ad.title, 
                            'owner': ad.user_id, 
                            'creation_time': ad.created_at, 
                            'description': ad.description})

    def patch(self, ad_id: int):
        json_data = validate(request.json, AdPatching) 
        with Session() as session:
            ad = get_ad(ad_id, session)
            for key, value in json_data.items():
                setattr(ad, key, value)
            session.add(ad)
            session.commit()
            return jsonify({'status': 'successfully patched'})

    def delete(self, ad_id: int):
        with Session() as session: 
            ad = get_ad(ad_id, session)
            session.delete(ad)
            session.commit()
            return jsonify({'status': 'successfully deleted'})
        

class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session: 
            user = get_user(user_id, session)
            return jsonify({'id': user.id, 'email': user.email})
    
    def post(self):
        json_data = validate(request.json, UserCreation)
        json_data['password'] = hash_password(json_data['password'])
        with Session() as session: 
            user = User(**json_data)
            session.add(user)
            try: 
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, 'E-mail already exists')
            return jsonify({'id': user.id, 'email': user.email})
        
    def patch(self, user_id: int):
        json_data = validate(request.json, UserPatching)
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password']) 
        with Session() as session:
            user = get_user(user_id, session)
            for key, value in json_data.items():
                setattr(user, key, value)
            session.add(user)
            session.commit()
            return jsonify({'status': 'successfully patched'})

    def delete(self, user_id: int):
        with Session() as session: 
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
            return jsonify({'status': 'successfully deleted'})


app.add_url_rule('/ads/<int:ad_id>/', view_func=AdView.as_view('ad_details'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/ads/', view_func=AdView.as_view('ads'), methods=['POST'])

app.add_url_rule('/users/<int:user_id>/', view_func=UserView.as_view('user_details'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UserView.as_view('users'), methods=['POST'])


if __name__ == '__main__':
    app.run(port=5005) 