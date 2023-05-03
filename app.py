from flask import Flask
from routes import init_routes
from helpers import *
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
logging.getLogger('flask_cors').level = logging.DEBUG
init_routes(app)



if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True)
