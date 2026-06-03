from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]


# GET - retrieve all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


# GET - retrieve a single user by id
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


# POST - create a new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_id = max((u["id"] for u in users), default=0) + 1
    user = {"id": new_id, "name": data["name"]}
    users.append(user)
    return jsonify(user), 201


# PUT - update an existing user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user["name"] = data["name"]
    return jsonify(user)


# DELETE - remove a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted"})


if __name__ == "__main__":
    app.run(debug=True)
