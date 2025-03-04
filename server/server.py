from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
groups = []
students = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
        {"id": 4, "name": "David"},
        {"id": 5, "name": "Eve"},
    ]
current_group_id = 0

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    return jsonify(groups)

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group_by_id(group_id):
    """
    Route to get a group by ID
    param group_id: The ID of the group to retrieve
    return: Group object or 404 if not found
    """
    group = next((g for g in groups if g["id"] == group_id), None)
    if group is None:
        abort(404, description="Group not found")
    return jsonify(group)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    return jsonify(students)

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    for group in groups:
        if group['id'] == group_id:
            groups.remove(group)
    
    return '', 204  # Return 204 (do not modify this line)

@app.errorhandler(400)
def handle_400_error(e):
    return jsonify({"error": e.description}), 400

def ensure_unique_group_name(base_name: str) -> str:
    """
    Check if groupName already exists. If it does, add (1), (2) ... until a non-existent name is found.
    """
    candidate_name = base_name
    i = 1
    while any(g["groupName"] == candidate_name for g in groups):
        candidate_name = f"{base_name}({i})"
        i += 1
    return candidate_name

@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """
    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
     
    if not group_name or not isinstance(group_members, list):
        abort(400, description = "groupName and members must be provided")

    # Check if the group name already exists
    group_name = ensure_unique_group_name(group_name)
    
    new_members = []
    # For each member name, check if the student already exists, if not create a new student record
    for member in group_members:
        existing_student = next((s for s in students if s["name"] == member), None)
        if existing_student:
            new_members.append(existing_student)
        else:
            new_student = {"id": len(students) + 1, "name": member}
            students.append(new_student)
            new_members.append(new_student)
    
    new_group = {
        "id": len(groups) + 1,
        "groupName": group_name,
        "members": new_members,
    }
    groups.append(new_group)
    
    return jsonify(new_group), 201

if __name__ == '__main__':
    app.run(port=3902, debug=True)