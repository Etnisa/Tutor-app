from flask import make_response, jsonify
import requests


def forward_response(r):
    cookies = r.cookies.get_dict()
    resp = make_response(jsonify(r.json()), r.status_code)
    for c in cookies:
        resp.set_cookie(c, cookies[c])
    return resp


def get_annocements():
    return requests.get("https://chatty-bulldog-76.telebit.io/announcements").json()



def filter_annoucements(search_for: str):
    annocements = get_annocements()
    filtered = []
    for a in annocements:
        if str(a.values()).find(search_for) >= 0:
            filtered.append(a)
    return filtered
