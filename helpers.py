import json

from flask import make_response, jsonify
import requests
from constants import *
import base64

avatar_cache = {}
subjects_cache = None


def forward_response(r):
    cookies = r.cookies.get_dict()
    resp = make_response(jsonify(r.json()), r.status_code)
    for c in cookies:
        resp.set_cookie(c, cookies[c])
    return resp


def get_annocements(params=''):
    announcements = requests.get(
        f"{API}/announcements{params}"
    ).json()

    # cut title
    for a in announcements:
        a["short_title"] = a["title"]
        if len(a["title"]) > MAX_TITLE_LEN:
            a["short_title"] = a["title"][:MAX_TITLE_LEN] + "..."

    return announcements


def filter_annoucements(search_for):
    search_for = search_for.lower()
    search_for = search_for.split()
    annocements = get_annocements(params='?price_sort=asc')
    if len(search_for) == 0:
        return annocements
    filtered = []
    for a in annocements:
        values = str(a.values())
        values = values.lower()

        add = True
        for s in search_for:
            if values.find(s) < 0:
                add = False

        if add:
            filtered.append(a)

    return filtered


def get_user_annoucements(user):
    user_annoucements = []
    annoucements = get_annocements()
    for a in annoucements:
        if a["announcer_username"] == str(user):
            user_annoucements.append(a)

    return user_annoucements


def get_my_account(request):
    r = requests.get(
        f"{API}/my_account", cookies=request.cookies
    )
    return r.json()


def get_avatar(username):
    if username in avatar_cache.keys():
        avatar = avatar_cache[username]
        print(f"{username} avatar read from cache")
    else:
        avatar = requests.get(f"{API}/user/{username}/avatar").json()
        # default avatars are not cached
        if len(avatar_cache) < AVATAR_CACHE_SIZE and avatar is not None:
            avatar_cache[username] = avatar
        print(f"{username} avatar read from api")
    return avatar


def get_subjects():
    global subjects_cache
    if subjects_cache is None:
        subjects_cache = get_subjects_api()
    print("read subjects from cache")
    return json.dumps(subjects_cache)


def get_subjects_api() -> dict:
    subjects = requests.get(f"{API}/subjects").json()
    result = {s['degree_course']: {} for s in subjects}
    for s in subjects:
        result[s['degree_course']][s['subject']] = []

    for s in subjects:
        result[s['degree_course']][s['subject']].append(s['semester'])
    print("read subjects from api")

    return result
