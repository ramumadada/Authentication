from flask import Flask, request, jsonify

app = Flask(__name__)

# Per-resource ACL: resource -> {user: set(permissions)}
ACL = {
    "device-42-log": {"alice": {"read", "write"}, "bob": {"read"}},
    "device-99-log": {"alice": {"read"}},
}

@app.route("/logs/<resource>", methods=["GET"])
def read_log(resource):
    user = request.headers.get("X-User")
    perms = ACL.get(resource, {}).get(user, set())
    if "read" not in perms:
        return jsonify({"error": f"'{user}' has no read access to '{resource}'"}), 403
    return jsonify({"msg": f"log contents of {resource}"})

@app.route("/logs/<resource>", methods=["DELETE"])
def delete_log(resource):
    user = request.headers.get("X-User")
    perms = ACL.get(resource, {}).get(user, set())
    if "write" not in perms:
        return jsonify({"error": f"'{user}' has no write access to '{resource}'"}), 403
    return jsonify({"msg": f"{resource} deleted"})

if __name__ == "__main__":
    app.run(port=5000)
