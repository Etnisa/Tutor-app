from flask import render_template, request 
import requests
from helpers import forward_response

def init_routes(app):
    @app.route('/test')
    def test(): 
        return render_template('test.html')
    
    @app.route('/')
    def main():
        announcements = requests.get('https://chatty-bulldog-76.telebit.io/announcements').json()
        for a in announcements:
            a['short_title']=a['title']
            if len(a['title']) > 40:
                a['short_title']=a['title'][:40]+'...'   
        return render_template('index.html', announcements=announcements)

    @app.route('/announcements', methods=["GET"])
    def announcements():
        r = requests.get('https://chatty-bulldog-76.telebit.io/announcements')
        return r.json()

    @app.route('/login', methods=["POST"])
    def login():
        r = requests.post(
            'https://chatty-bulldog-76.telebit.io/login',
            headers={'Content-Type': 'application/json'},
            json={'user': 't2',
                'password': 't1'}                  
        )
        return forward_response(r)

    @app.route('/my_account', methods=["GET"])
    def my_account():
        r = requests.get('https://chatty-bulldog-76.telebit.io/my_account', cookies=request.cookies)
        return r.json()
