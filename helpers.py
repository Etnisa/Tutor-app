from flask import make_response, jsonify


def forward_response(r):
    cookies = r.cookies.get_dict()
    resp = make_response(jsonify(r.json()),r.status_code)
    for c in cookies:
        resp.set_cookie(c, cookies[c])
    return resp
