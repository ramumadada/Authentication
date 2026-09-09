from flask import Flask, request, jsonify
import time

app = Flask(__name__)
CLIENTS = {"edge-device-1": "device-secret-123"}
tokens = {}

@app.route("/oauth/token", methods=["POST"])
def token():
    client_id = request.form.get("client_id")
    client_secret = request.form.get("client_secret")
    if CLIENTS.get(client_id) != client_secret:
        return jsonify({"error": "invalid_client"}), 401
    access_token = f"token-{client_id}-{int(time.time())}"
    tokens[access_token] = client_id
    return jsonify({"access_token": access_token, "token_type": "Bearer", "expires_in": 3600})

@app.route("/sensor-data")
def sensor_data():
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "")
    if token not in tokens:
        return jsonify({"error": "invalid_token"}), 401
    return jsonify({"msg": f"Access granted to {tokens[token]}"})

if __name__ == "__main__":
    app.run(port=5000)
