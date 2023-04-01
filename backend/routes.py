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
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic.get("id") == id:
            return jsonify(pic), 200
    else:
        return {"error": "pic not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    new_id = new_picture.get("id")
    if new_id in [pic.get("id") for pic in data]:
        return {"Message": f"picture with id {new_id} already present"}, 302
    data.append(new_picture)
    return new_picture, 201
    

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_pic = request.json
    new_pic_id = new_pic.get("id")
    for pic in data:
        if pic.get("id") == new_pic_id:
            pic.update(new_pic)
            return new_pic, 200
    else:
        return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    delete_index = None
    for index, pic in enumerate(data):
        
        if pic.get("id") == id:
            delete_index = index
    if delete_index is not None:
        data.pop(delete_index)
        return {}, 204
    return {"message": "picture not found"}, 404

