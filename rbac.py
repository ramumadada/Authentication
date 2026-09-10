from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Pretend "database": user -> role
USER_ROLES = {"alice": "admin", "bob": "editor", "carol": "viewer"}

# Role -> allowed actions
ROLE_PERMISSIONS = {
    "admin":  {"read", "write", "delete"},
    "editor": {"read", "write"},
    "viewer": {"read"},
}

def require_permission(action):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            username = request.headers.get("X-User")  # simulate an authenticated user
            role = USER_ROLES.get(username)
            if not role or action not in ROLE_PERMISSIONS.get(role, set()):
                return jsonify({"error": f"'{username}' (role={role}) cannot '{action}'"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/document", methods=["GET"])
@require_permission("read")
def read_doc():
    return jsonify({"msg": "document content"})

@app.route("/document", methods=["DELETE"])
@require_permission("delete")
def delete_doc():
    return jsonify({"msg": "document deleted"})

if __name__ == "__main__":
    app.run(port=5000)
