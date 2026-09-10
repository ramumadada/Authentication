import jwt
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)
SECRET = "dev-secret"

def make_token(user, scopes):
    return jwt.encode({"user": user, "scope": " ".join(scopes)}, SECRET, algorithm="HS256")

# Pre-issue two example tokens so you can test immediately
TOKENS = {
    "device_reader": make_token("edge-device-1", ["read:sensors"]),
    "device_writer": make_token("edge-device-2", ["read:sensors", "write:config"]),
}

def require_scope(needed_scope):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "").replace("Bearer ", "")
            try:
                decoded = jwt.decode(auth, SECRET, algorithms=["HS256"])
            except jwt.InvalidTokenError:
                return jsonify({"error": "invalid token"}), 401
            token_scopes = decoded.get("scope", "").split()
            if needed_scope not in token_scopes:
                return jsonify({"error": f"token missing required scope '{needed_scope}'"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/sensors")
@require_scope("read:sensors")
def read_sensors():
    return jsonify({"msg": "sensor data"})

@app.route("/config", methods=["POST"])
@require_scope("write:config")
def write_config():
    return jsonify({"msg": "config updated"})

@app.route("/tokens")   # helper endpoint just so you can grab the demo tokens
def tokens():
    return jsonify(TOKENS)

if __name__ == "__main__":
    app.run(port=5000)

