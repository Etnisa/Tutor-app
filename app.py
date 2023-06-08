from flask import Flask, Response, request
from routes import init_routes
from flask_cors import CORS
import logging


app = Flask(__name__)
app.secret_key = 'super secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
CORS(app, supports_credentials=True)

logging.getLogger("flask_cors").level = logging.DEBUG

init_routes(app)

if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True)
