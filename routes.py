from flask import render_template, request, jsonify, redirect
import requests
from helpers import forward_response, get_annocements, filter_annoucements
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

        # cut title
        for a in announcements:
            a["short_title"] = a["title"]
            if len(a["title"]) > MAX_TITLE_LEN:
                a["short_title"] = a["title"][:MAX_TITLE_LEN] + "..."

        return render_template("index.html", announcements=announcements, pages=pages, page=page)

    @app.route("/announcements", methods=["GET"])
    def announcements():
        return get_annocements()

    @app.route("/announcement/<int:id>", methods=["GET"])
    def announcement(id):
        annoucement = requests.get(
            f"https://chatty-bulldog-76.telebit.io/announcements/{id}"
        ).json()
        annoucement = annoucement[0]
        response = jsonify(render_template("annoucement.html", a=annoucement))
        response.headers.add("Access-Control-Allow-Origin", "*")
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
