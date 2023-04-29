from flask import Flask, render_template, jsonify, make_response, request    
import requests

app = Flask(__name__)

@app.route('/')
def main():
    announcements = requests.get('https://chatty-bulldog-76.telebit.io/announcements').json()
    print(announcements[0])
    return render_template('index.html', announcements=announcements)

@app.route('/test')
def test(): 
    return render_template('test.html')


@app.route('/announcements', methods=["GET"])
def announcements():
    r = requests.get('https://chatty-bulldog-76.telebit.io/announcements')
    return r.json()

@app.route('/login', methods=["POST"])
def login():
    r = requests.post(
        'https://chatty-bulldog-76.telebit.io/login',
        headers={'Content-Type': 'application/json'},
        cookies=request.cookies,
        json={'user': 't1',
              'password': 't1'}                  
    )
    return r.json()


@app.route('/my_account', methods=["GET"])
def my_account():
    r = requests.get('https://chatty-bulldog-76.telebit.io/my_account', cookies=request.cookies)
    return r.json()
    

    
if __name__ == '__main__':
    app.run(debug=True)