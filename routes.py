from flask import render_template, request,jsonify
import requests
from helpers import forward_response, get_annocements, filter_annoucements
from constants import *


def init_routes(app):
    @app.route("/test")
    def test():
        return render_template("test.html")

    @app.route("/", methods=["GET", "POST"])
    def main():
        filter = ""
        if 'filter' in request.form.keys():
            filter = request.form['filter']
        announcements = filter_annoucements(filter)
        
        for a in announcements:
            a["short_title"] = a["title"]
            if len(a["title"]) > MAX_TITLE_LEN :
                a["short_title"] = a["title"][:MAX_TITLE_LEN] + "..."
                
        print("Zwrócone rekordy spełniające kryterium "+filter+" "+str(len(announcements)))
                
        return render_template("index.html", announcements=announcements)

    @app.route("/announcements", methods=["GET"])
    def announcements():
        return get_annocements()
    
    
    @app.route("/announcement/<int:id>", methods=["GET"])
    def announcement(id):  
        annoucement = requests.get(f"https://chatty-bulldog-76.telebit.io/announcements/{id}").json()
        annoucement = annoucement[0]
        response = jsonify(render_template("annoucement.html", a=annoucement))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route("/login", methods=["POST"])
    def login():
        r = requests.post(
            "https://chatty-bulldog-76.telebit.io/login",
            headers={"Content-Type": "application/json"},
            json={"user": "t2", "password": "t1"},
        )
        return forward_response(r)

    @app.route("/my_account", methods=["GET"])
    def my_account():
        r = requests.get(
            "https://chatty-bulldog-76.telebit.io/my_account", cookies=request.cookies
        )
        return r.json()
