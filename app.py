from flask import Flask
from routes import init_routes

app = Flask(__name__)
init_routes(app)  
    
if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
