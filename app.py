from flask import Flask
from flask_cors import CORS

import secrets  # For generating a secure secret key
from api.recommendation import recommendation_route, unpublished_route

from config import ProdConfig

app = Flask(__name__)

app.config.from_object(ProdConfig)
app.register_blueprint(recommendation_route)
app.register_blueprint(unpublished_route)

# Generate a cryptographically secure secret key (store securely outside code)
app.secret_key = secrets.token_urlsafe(32)
print(app.secret_key)

CORS(app)


if __name__ == '__main__':
    app.run(debug=True, port=5002)