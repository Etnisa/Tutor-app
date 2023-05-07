from flask import render_template, request, jsonify, redirect, make_response, Response
import requests
from helpers import (
    forward_response,
    get_annocements,
    filter_annoucements,
    get_user_annoucements,
    get_my_account,
)
from constants import *
import math
from flask_cors import cross_origin


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
        
        # get account data
        account_data = get_my_account(request)

        return render_template(
            "index.html", announcements=announcements, pages=pages, page=page, account_data=account_data
        )

    @app.route("/announcements", methods=["GET"])
    def announcements():
        return get_annocements()

    # @cross_origin()
    @app.route("/account/<user>", methods=["GET", "POST"])
    def account(user):
        announcements_list = get_user_annoucements(user)
        account_data = get_my_account(request)

        # is it me
        is_it_me = False

        if "username" in account_data.keys() and account_data["username"] == user:
            is_it_me = True

        # print(is_it_me,account_data['username'],user)

        # reviews
        reviews = []
        if "reviews" in account_data.keys():
            reviews = account_data["reviews"]

        return render_template(
            "account.html",
            announcements_list=announcements_list,
            account_data=account_data,
            is_it_me=is_it_me,
            reviews=reviews,
        )

    # @cross_origin()
    @app.route("/account_edit", methods=["GET"])
    def account_edit():
        account_data = get_my_account(request)
        print(request.cookies)
        response = jsonify(
            render_template("account_edit.html", account_data=account_data)
        )
        # response.headers.add("Access-Control-Allow-Origin", "localhost:5000")
        # response.headers.add("Access-Control-Allow-Credentials", "true")
        # response.headers.add("Access-Control-Allow-Methods", "GET")
        # print(account_data)
        return response

    @app.route("/announcement/<int:id>", methods=["GET"])
    def announcement(id):
        annoucement = requests.get(
            f"https://chatty-bulldog-76.telebit.io/announcements/{id}"
        ).json()
        annoucement = annoucement[0]
        response = jsonify(render_template("annoucement.html", a=annoucement))
        response.headers.add(
            "Access-Control-Allow-Origin", "http://127.0.0.1:5000/account_edit"
        )
        return response

    @app.route("/announcement", methods=["POST"])
    def announcement_add():
        annoucement = requests.post(
            f"https://chatty-bulldog-76.telebit.io/announcements",
            headers={"Content-Type": "application/json"},
            json={
                "title": "Ucze jak robić równania różniczkowe",
                "content": "fajny opis",
                "price": 120,
                "is_negotiable": False,
                "degree_course": "informatyka",
                "subject": "matematyka",
                "semester": 4
                }
        ).json()
        return ""
    

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
        if r.status_code == 200:
            resp = make_response(redirect(f"/account/{get_my_account(r)['username']}", 302))
            cookies = r.cookies.get_dict()
            for c in cookies:
                resp.set_cookie(c, cookies[c])
        # login error
        else:
            resp = make_response(redirect("/", 302))
            resp.set_cookie('login_err', '1')
        return resp

    @app.route("/my_account", methods=["GET"])
    def my_account():
        return get_my_account(request)

    @app.route("/register", methods=["POST"])
    def register():
        r = requests.post(
            "https://chatty-bulldog-76.telebit.io/sign_up",
            headers={"Content-Type": "application/json"},
            json={
                "username": request.form["username"],
                "email": request.form["email"],
                "password": request.form["password"],
                "name": request.form["name"],
                "surname": request.form["surname"],
            },
        )
        return forward_response(r)

    @app.route("/logout", methods=["GET"])
    def logout():
        r = requests.get("https://chatty-bulldog-76.telebit.io/logout")
        resp = make_response(redirect('/',302))
        resp.set_cookie('session', '', expires=0)
        return resp
    


    # @app.route("/edit_acc", methods=["PUT"])
    # def edit_acc():
    #     r = requests.post(
    #         "https://chatty-bulldog-76.telebit.io/my_account",
    #         headers={"Content-Type": "application/json"}, # DO SPRAWDZENIA PRZEZ KAMILA
    #         json={
    #             "description":request.form[''],
    #             "email": request.form[''],
    #             "name": request.form[''],
    #             "phone": request.form[''],
    #             "surname": request.form[''],
    #             "semester": request.form[''],
    #             "degree_course":request.form[''] 
    #         }
    #     )
    # return 