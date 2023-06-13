from flask import (
    render_template,
    request,
    jsonify,
    redirect,
    make_response,
    Response,
    flash,
)
import requests
from constants import *
import math
from helpers import *
import base64
import json


def init_routes(app):
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
                        (page - 1) * CARDS_PER_PAGE: page * CARDS_PER_PAGE
                        ]

        # get account data
        account_data = get_my_account(request)

        # get avatars
        avatars = {}
        for a in announcements:
            username = a['announcer_username']
            if username not in avatars.keys():
                avatars[username] = get_avatar(username)
        # print(avatars)

        return render_template(
            "index.html",
            announcements=announcements,
            pages=pages,
            page=page,
            account_data=account_data,
            avatars=avatars
        )

    @app.route("/announcements", methods=["GET"])
    def announcements():
        return get_annocements(params='?price_sort=asc')

    # @cross_origin()
    @app.route("/account/<user>", methods=["GET", "POST"])
    def account(user):
        announcements_list = get_user_annoucements(user)
        account_data = get_my_account(request)
        profile = requests.get(f"{API}/user/{user}", cookies=request.cookies).json()

        # is it me
        is_it_me = False

        if "username" in account_data.keys() and account_data["username"] == user:
            is_it_me = True

        # print(is_it_me,account_data['username'],user)

        # reviews
        reviews = []
        if "reviews" in profile.keys():
            reviews = profile["reviews"]

        # avatar
        avatar = get_avatar(profile['username'])

        return render_template(
            "account.html",
            announcements_list=announcements_list,
            account_data=account_data,
            is_it_me=is_it_me,
            reviews=reviews,
            profile=profile,
            avatar=avatar
        )

    # @cross_origin()
    @app.route("/account_edit", methods=["GET"])
    def account_edit():
        account_data = get_my_account(request)
        degree_courses = json.loads(get_subjects())
        degree_courses = degree_courses.keys()
        response = jsonify(
            render_template("account_edit.html", account_data=account_data, degree_courses=degree_courses)
        )
        # response.headers.add("Access-Control-Allow-Origin", "localhost:5000")
        # response.headers.add("Access-Control-Allow-Credentials", "true")
        # response.headers.add("Access-Control-Allow-Methods", "GET")
        # print(account_data)
        return response

    @app.route("/announcement/<int:id>", methods=["GET"])
    def announcement(id):
        annoucement = requests.get(
            f"{API}/announcements/{id}"
        ).json()
        annoucement = annoucement[0]

        username = annoucement['announcer_username']
        avatar = get_avatar(username)

        response = jsonify(render_template("annoucement.html", a=annoucement, avatar=avatar))
        response.headers.add(
            "Access-Control-Allow-Origin", "http://127.0.0.1:5000/account_edit"
        )
        return response

    @app.route("/announcement_edit/<int:id>", methods=["GET"])
    def announcement_edit(id):
        annoucement = requests.get(
            f"{API}/announcements/{id}"
        ).json()
        annoucement = annoucement[0]
        response = jsonify(render_template("announcement_edit.html", a=annoucement, subjects=get_subjects()))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route("/add_ann_modal", methods=["GET"])
    def add_ann_modal():
        response = jsonify(render_template("announcement_add.html", subjects=get_subjects()))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route("/add_ann", methods=["POST"])
    def announcement_add():
        # check if all form files are given
        for key in ['title', 'comment', 'price', 'degree_course', 'subject', 'semester']:
            if key not in request.form.keys() or request.form[key] == '':
                flash("Błędne dane. Nie uzupełniono wszystkich pól formularza!")
                resp = make_response(redirect(f"/account/{get_my_account(request)['username']}", 302))
                return resp

        # set is negotiable to True if checkbox is checked
        is_negotiable = False
        if 'neg' in request.form.keys() and request.form['neg'] == "on":
            is_negotiable = True

        r = requests.post(
            f"{API}/announcements",
            cookies=request.cookies,
            headers={"Content-Type": "application/json"},
            json={
                "title": request.form['title'],
                "content": request.form['comment'],
                "price": int(request.form['price']),
                "is_negotiable": is_negotiable,
                "degree_course": request.form['degree_course'],
                "subject": request.form['subject'],
                "semester": int(request.form['semester']),
            }
        )

        if r.status_code == 200:
            resp = make_response(redirect(f"/account/{get_my_account(request)['username']}", 302))

        else:
            # TODO flash error
            flash("Błędne dane")
            resp = make_response(redirect(f"/account/{get_my_account(request)['username']}", 302))
        return resp

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
            f"{API}/login",
            headers={"Content-Type": "application/json"},
            json={
                "user": request.form["username"],
                "password": request.form["password"],
            },
        )

        # login success
        if r.status_code == 200:
            resp = make_response(
                redirect(f"/account/{get_my_account(r)['username']}", 302)
            )
            cookies = r.cookies.get_dict()
            for c in cookies:
                resp.set_cookie(c, cookies[c])
        # login error
        else:
            resp = make_response(redirect("/", 302))
            resp.set_cookie("login_err", "1")
        return resp

    @app.route("/my_account", methods=["GET"])
    def my_account():
        return get_my_account(request)

    @app.route("/register", methods=["POST"])
    def register():
        r = requests.post(
            f"{API}/sign_up",
            headers={"Content-Type": "application/json"},
            json={
                "username": request.form['username'],
                "email": request.form['email'],
                "password": request.form['password'],
                "name": request.form['name'],
                "surname": request.form['surname'],
            }
        )
        # TODO login and redirect to profil page
        return redirect(f"/", 302)

    @app.route("/logout", methods=["GET"])
    def logout():
        r = requests.get(f"{API}/logout")
        resp = make_response(redirect("/", 302))
        resp.set_cookie("session", "", expires=0)
        return resp

    @app.route("/edit_acc", methods=["POST"])
    def edit_acc():
        r = requests.put(
            f"{API}/my_account",
            cookies=request.cookies,
            headers={"Content-Type": "application/json"},
            json={
                "description": request.form["content"],
                "email": request.form["email"],
                "name": request.form["name"],
                "phone": request.form["phone"],
                "surname": request.form["surname"],
                "semester": int(request.form["semester"]),
                "degree_course": request.form["degree_course"],
            },
        )
        username = get_my_account(request)['username']

        if r.status_code == 200:
            resp = make_response(redirect(f"/account/{username}", 302))
        else:
            # TODO flash error
            flash("Błędne dane")
            resp = make_response(redirect(f"/account/{username}", 302))
            print("ACHTUNG GRANADE")

        # file
        if request.files['file'].filename:
            r = requests.put(
                f"{API}/my_account/avatar",
                cookies=request.cookies,
                files=request.files
            )

            if r.status_code == 200:
                resp = make_response(redirect(f"/account/{username}", 302))
                # delete cached avatar
                if username in avatar_cache.keys():
                    avatar_cache.pop(username)
            else:
                print(r.content)
                # TODO flash error
                flash(
                    "Błąd pliku.Upewnij się że przesyłasz plik w formacie png lub jpg o rozdzielczości nie większej niż 512x512px.")
                resp = make_response(redirect(f"/account/{username}", 302))
                print("ACHTUNG GRANADE")

        return resp

    @app.route("/edit_ann", methods=["POST"])
    def ann_edit():
        id = request.form["id"]
        is_negotiable = False
        if 'neg' in request.form.keys() and request.form['neg'] == "on":
            is_negotiable = True

        r = requests.put(
            f"{API}/announcements/{id}",
            cookies=request.cookies,
            headers={"Content-Type": "application/json"},
            json={
                "title": request.form["title"],
                "content": request.form["content"],
                "price": int(request.form["price"]),
                "is_negotiable": is_negotiable,
                "degree_course": request.form["degree_course"],
                "subject": request.form["subject"],
                "semester": int(request.form["semester"]),
            }
        )
        if r.status_code == 200:
            resp = make_response(redirect(f"/account/{get_my_account(request)['username']}", 302))

        else:
            # TODO flash error
            flash("Błędne dane")
            resp = make_response(redirect(f"/account/{get_my_account(request)['username']}", 302))
            print("ACHTUNG GRANADE")
        return resp

    @app.route("/del_ann/<id>", methods=["POST"])
    def del_edit(id):
        print(request.cookies.get('session'))
        r = requests.delete(
            f"{API}/announcements/{id}",
            cookies=request.cookies
        )
        # if r.status_code == 200:
        #     # resp = make_response(redirect(f"/account/{get_my_account(request)['username']}", 302))
        #     resp = make_response(redirect("/",302))
        # else:
        #     # TODO flash error
        #     flash("Błędne dane")
        #     resp = make_response(redirect(f"/account/{get_my_account(request)['username']}", 302))
        # return resp
        return ""

    @app.route("/add_review", methods=["POST"])
    def add_review():
        username = request.form.get('username')
        r = requests.post(
            f"{API}/user/{username}/review",
            cookies=request.cookies,
            headers={"Content-Type": "application/json"},
            json={
                "rate": int(request.form.get('rate')),
                "review": request.form.get('review_content')
            }
        )

        if r.status_code == 200:
            resp = make_response(redirect(f"/account/{username}", 302))

        else:
            # TODO flash error
            flash("Błędne dane")
            resp = make_response(redirect(f"/account/{get_my_account(request)['username']}", 302))
        return resp
