from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures."""
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by its ID."""
    # Find the picture with the given ID
    picture = next((item for item in data if item["id"] == id), None)
    
    # If found, return the picture
    if picture:
        return jsonify(picture), 200
    # If not found, return a 404 error
    else:
        abort(404, description="Picture not found")


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["POST"])
def create_picture(id):
    """Create a picture with the specified ID."""
    # Extract the picture data from the request body
    picture_data = request.json
    
    # Check if a picture with the given ID already exists in the data list
    existing_picture = next((item for item in data if item["id"] == id), None)
    
    if existing_picture:
        # If the picture with the ID already exists, return a 302 status code with a message
        return jsonify({"Message": f"picture with id {id} already present"}), 302
    else:
        # If not, append the new picture data to the data list and return it with a 201 status code
        data.append(picture_data)
        return jsonify(picture_data), 201



######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture with the specified ID."""
    # Extract the updated picture data from the request body
    updated_picture_data = request.json
    
    # Find the picture with the given ID in the data list
    existing_picture = next((item for item in data if item["id"] == id), None)
    
    if existing_picture:
        # Update the picture data in the list
        index = data.index(existing_picture)
        data[index] = updated_picture_data
        return jsonify(data[index]), 200
    else:
        # If the picture doesn't exist, return a 404 error with a message
        return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture with the specified ID."""
    # Find the picture with the given ID in the data list
    existing_picture = next((item for item in data if item["id"] == id), None)
    
    if existing_picture:
        # Remove the picture from the list
        data.remove(existing_picture)
        # Return a 204 status code with an empty body
        return make_response('', 204)
    else:
        # If the picture doesn't exist, return a 404 error with a message
        return jsonify({"message": "picture not found"}), 404

@app.route("/picture", methods=["POST"])
def create_picture_without_id():
    picture_data = request.json
    existing_picture = next((item for item in data if item["id"] == picture_data["id"]), None)
    
    if existing_picture:
        return jsonify({"Message": f"picture with id {picture_data['id']} already present"}), 302
    
    data.append(picture_data)
    return jsonify(picture_data), 201
