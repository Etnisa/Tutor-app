from flask import make_response, jsonify
import requests
from constants import *


def forward_response(r):
    cookies = r.cookies.get_dict()
    resp = make_response(jsonify(r.json()), r.status_code)
    for c in cookies:
        resp.set_cookie(c, cookies[c])
    return resp


def get_annocements():
    announcements = requests.get("https://chatty-bulldog-76.telebit.io/announcements").json()
    
     # cut title
    for a in announcements:
        a["short_title"] = a["title"]
        if len(a["title"]) > MAX_TITLE_LEN:
            a["short_title"] = a["title"][:MAX_TITLE_LEN] + "..."
        
    return announcements


def filter_annoucements(search_for):
    search_for = search_for.lower()
    search_for = search_for.split()
    annocements = get_annocements()
    if len(search_for) == 0:
        return annocements
    filtered = []
    for a in annocements:
        values = str(a.values())
        values = values.lower()
        
        add = True
        for s in search_for:
            if values.find(s) < 0:
                add= False
        
        if add: 
            filtered.append(a) 
            
    return filtered


def get_user_annoucements(user):
    user_annoucements = []
    annoucements = get_annocements()
    for a in annoucements:
        if a['announcer_username'] == str(user):
            user_annoucements.append(a)

    return user_annoucements

def get_my_account(request):
    r = requests.get(
            "https://chatty-bulldog-76.telebit.io/my_account", cookies=request.cookies
        )
    return r.json()