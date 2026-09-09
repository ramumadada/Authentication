import jwt, datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET = "dev-secret-change-me"
USERS = {"admin": "pass123"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if USERS.get(data.get("username")) == data.get("password"):
        payload = {
            "user": data["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        token = jwt.encode(payload, SECRET, algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/data")
def data():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401
    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return jsonify({"msg": f"Hello {decoded['user']}, token verified"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(port=5000)
