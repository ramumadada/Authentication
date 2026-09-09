from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)
USERS = {"admin": "pass123"}

def check_auth(username, password):
    return USERS.get(username) == password

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"error": "Unauthorized"}), 401, \
                {"WWW-Authenticate": 'Basic realm="Login Required"'}
        return f(*args, **kwargs)
    return decorated

@app.route("/data")
@requires_auth
def data():
    return jsonify({"msg": "You are authenticated via Basic Auth"})

if __name__ == "__main__":
    app.run(port=5000)
