from flask import render_template, request, jsonify, redirect, make_response
import requests
from helpers import forward_response, get_annocements, filter_annoucements, get_user_annoucements
from constants import *
import math


def init_routes(app):
    @app.route("/test")
    def test():
        return render_template("test.html")

    @app.route("/", methods=["GET", "POST"])
    def main():
        return redirect("/1", code=302)

    @app.route("/<int:page>", methods=["GET", "POST"])
    def page(page):        
        # filter annoucements
        filter = ""
        if "filter" in request.form.keys():
            filter = request.form["filter"]

        announcements = filter_annoucements(filter)

        # calculate pages qty
        pages = math.ceil(len(announcements) / CARDS_PER_PAGE)

        # limit anoucements qty
        announcements = announcements[
            (page - 1) * CARDS_PER_PAGE : page * CARDS_PER_PAGE
        ]

        return render_template(
            "index.html", announcements=announcements, pages=pages, page=page
        )

    @app.route("/announcements", methods=["GET"])
    def announcements():
        return get_annocements()

    @app.route("/account/<user>", methods=["GET"])
    def account(user):
        announcements_list = get_user_annoucements(user)
        return render_template('account.html', announcements_list=announcements_list)

    @app.route("/announcement/<int:id>", methods=["GET"])
    def announcement(id):
        annoucement = requests.get(
            f"https://chatty-bulldog-76.telebit.io/announcements/{id}"
        ).json()
        annoucement = annoucement[0]
        response = jsonify(render_template("annoucement.html", a=annoucement))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route("/login_modal", methods=["GET"])
    def login_modal():
        response = jsonify(render_template("login.html"))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route("/register_modal", methods=["GET"])
    def register_modal():
        response = jsonify(render_template("register.html"))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    @app.route("/login", methods=["POST"])
    def login():
        r = requests.post(
            "https://chatty-bulldog-76.telebit.io/login",
            headers={"Content-Type": "application/json"},
            json={
                "user": request.form['username'],
                "password": request.form['password']
                }
        )
        
        # login success
        resp = make_response(redirect('/',302))
        if r.status_code == 200:

            cookies = r.cookies.get_dict()
            for c in cookies:
                resp.set_cookie(c, cookies[c])
        # login error
        else:
            resp.set_cookie('login_err', '1')
        return resp
            

    @app.route("/my_account", methods=["GET"])
    def my_account():
        r = requests.get(
            "https://chatty-bulldog-76.telebit.io/my_account", cookies=request.cookies
        )
        return r.json()

    @app.route("/register", methods=["POST"])
    def register():
        r = requests.post(
            "https://chatty-bulldog-76.telebit.io/sign_up",
            headers={"Content-Type": "application/json"},
            json={
                "username": request.form['username'],
                "email": request.form['email'],
                "password": request.form['password'],
                "name": request.form['name'],
                "surname": request.form['surname'],
            }
        )
        return forward_response(r)
    