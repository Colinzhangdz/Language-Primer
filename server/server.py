from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# In-memory data storage
groups = [
    {
        "id": 1,
        "groupName": "Group 1",
        "members": [1, 2, 3],
    },
    {
        "id": 2,
        "groupName": "Group 2",
        "members": [4, 5],
    },
]

students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
]
@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    # TODO: (sample response below)
    return jsonify(groups)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    # TODO: (sample response below)
    return jsonify(students)

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
    
    # TODO: implement storage of a new group and return their info (sample response below)

    new_id = max(group["id"] for group in groups) + 1 if groups else 1

    # Create the new group
    new_group = {
        "id": new_id,
        "groupName": group_name,
        "members": group_members,
    }

    # Add the new group to the list
    groups.append(new_group)

    return jsonify(new_group), 201

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    # TODO: (delete the group with the specified id)
    global groups
    groups = [group for group in groups if group["id"] != group_id]
    return '', 204  # Return 204 (do not modify this line)

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    group = next((group for group in groups if group["id"] == group_id), None)
    
    if group is None:
        abort(404, "Group not found")

    # Get member details
    member_details = []
    for member_id in group["members"]:
        member = next((student for student in students if student["id"] == member_id), None)
        if member:
            member_details.append(member)

    # Return the group with member details
    return jsonify({
        "id": group["id"],
        "groupName": group["groupName"],
        "members": member_details,
    })
    # TODO:
    # if group id isn't valid:
    #     abort(404, "Group not found")

if __name__ == '__main__':
    app.run(port=3902, debug=True)
