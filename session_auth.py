from flask import Flask, request, session, jsonify

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"
USERS = {"admin": "pass123"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if USERS.get(data.get("username")) == data.get("password"):
        session["user"] = data["username"]   # Flask signs this into a cookie
        return jsonify({"msg": "Logged in"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/data")
def data():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({"msg": f"Hello {session['user']}, session is active"})

if __name__ == "__main__":
    app.run(port=5000)
