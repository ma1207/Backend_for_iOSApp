import json

import db

#from db import db
from flask import Flask
from flask import request

#from db import Internship
#from db import Subtask
#from db import Category

#db_filename = "list.db"
app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True

# db.init_app(app)
# with app.app_context():
#     db.create_all()

# def success_response(body, code=200):
#      return json.dumps(body), code

# def failure_response(message, code=404):
#      return json.dumps({"error": message}), code

# @app.route("/")
# @app.route("/internships/")
# def get_internships():
#     return success_response({"internships": [i.serialize() for i in Internship.query.all()]})

# @app.route("/internships/", methods=["POST"])
# def create_internship():
#     body = json.loads(request.data)
#     new_internship = Internship(name = body.get("CompanyName"), status = body.get("ApplicationStatus"), date = body.get("InterviewDate"))
#     db.session.add(new_internship)
#     db.session.commit()
#     return success_response(new_internship.serialize(), 201)

# @app.route("/internships/<int:internship_id>/", methods = ["POST"])
# def get_internship(internship_id):
#     internship = Internship.query.filter_by(id=internship_id).first()
#     if internship is None:
#         return failure_response("Internship not found ")
#     return success_response(internship.serialize())

# @app.route("/internships/<int:internship_id>/", methods = ["POST"])
# def update_internship(internship_id):
#     body = json.loads(request.data)
#     internship = Internship.query.filter_by(id=internship_id).first()
#     if internship is None:
#         return failure_response("Internship not found ")
#     internship.name = body.get("CompanyName")
#     internship.status = body.get("ApplicationStatus")
#     internship.date = body.get("InterviewDate")
#     db.session.commmit()
#     return success_response(internship.serialize)


# @app.route("/internships/<int:internship_id>/", methods = ["DELETE"])
# def delete_internship(internship_id):
#     internship = Internship.query.filter_by(id=internship_id).first()
#     if internship is None:
#         return failure_response("Internship not found")
#     db.session.delete(internship)
#     db.session.commmit()
#     return success_response(internship.serialize())

# @app.route("/internships/<int:internship_id>/subtasks/", methods=["POST"])
# def create_subtask(internship_id):
#     internship = Internship.query.filter_by(id = internship_id).first()
#     if internship is None:
#         return failure_response("Internship not found")
#     body = json.loads(request.data)
#     new_subtask = Subtask(
#         title = body.get("title"),
#         description = body.get("description"),
#         date = body.get("date"),
#         internship_id = internship_id
#     )
#     db.session.add(new_subtask)
#     db.session.commit()
#     return success_response(new_subtask.serialize())

# @app.route("/internships/<int:internship_id>/category/", methods=["POST"])
# def assign_category(internship_id):
#     internship = internship.query.filter_by(id=internship_id).first()

#     if internship is None:
#         return failure_response("Task not found")

#     body = json.loads(request.data)
#     status = body.get("ApplicationStatus")

#     category = Category.query.filter_by(status=status)

#     if category is None:
#         category = Category(status=status)
    
#     internship.categories.append()
#     db.session.commit()
#     return success_response(internship.serialize())


DB = db.DatabaseDriver()

def success_response(body, code=200):
    return json.dumps(body), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

@app.route("/")
@app.route("/internships/")
def get_internships():
    return json.dumps(DB.get_all_internships())

@app.route("/internships/", methods= ["POST"])
def create_internship():
    body = json.loads(request.data)
    name = body.get("CompanyName")
    status = body.get("ApplicationStatus")
    date = body.get("InterviewDate")
    internship_id = DB.insert_internship_table(name, status, date)
    internship = DB.get_internship_by_id(internship_id)
    if internship is None:
        return json.dumps({"error": "Something went wrong while creating task!"}), 400
    return json.dumps(internship), 201

@app.route("/internships/<int:internship_id>/")
def get_internship(internship_id):
    internship = DB.get_internship_by_id(internship_id)
    if internship is None:
        return json.dumps({"error": "Internship not found"}), 404
    return json.dumps(internship), 200

@app.route("/internships/<int:internship_id>/", methods =["POST"])
def update_internship(internship_id):
    body = json.loads(request.data)
    name = body.get("CompanyName")
    status = body.get("ApplicationStatus")
    date = body.get("InterviewDate")

    DB.update_internship_by_id(internship_id, name, status, date)

    internship = DB.get_internship_by_id(internship_id)
    if internship is None:
        return json.dumps({"error": "Internship not found"}), 404
    return json.dumps(internship), 200


@app.route("/internships/<int:internship_id>/", methods=["DELETE"])
def delete_internship(internship_id):
    internship = DB.get_internship_by_id(internship_id)
    if internship is None:
        return json.dumps({"error": "Internship not found"}), 404
    DB.delete_internship_by_id(internship_id)
    return json.dumps(internship), 200

@app.route("/subtasks/")
def get_all_subtasks():
    return success_response({DB.get_all_subtasks})

@app.route("/internships/<int:internship_id>/subtasks/", methods=["POST"])
def create_subtask(internship_id):
    body = json.loads(request.data)
    name = body.get("CompanyName")
    status = body.get("ApplicationStatus")
    date = body.get("InterviewDate")

    internship = DB.get_internship_by_id(internship_id)

    if internship is None:
        return failure_response()

    subtask_id = DB.insert_subtask(name, status, date, internship_id)
    subtask = DB.get_subtask_by_id(subtask_id)

    if subtask is None:
        return failure_response()

    return success_response(subtask, 201)

@app.route("/internships/<int:internship_id>/subtasks/")
def get_all_subtasks_for_internship(internship_id):
    internship = DB.get_internship_by_id(internship_id)
    if internship is None:
        return failure_response("Task does not exist")
    subtasks = DB.get_subtasks_by_internship(internship_id)
    return success_response({"subtasks": subtasks})




#VERSION ONE
# internships = {
#     0:{
#         "id": 0,
#         "CompanyName": "Google",
#         "ApplicationStatus": "In Progress",
#         "InterviewDate": "10/20/2022"
#     },
#     1:{
#         "id": 1,
#         "CompanyName": "Google",
#         "ApplicationStatus": "In Progress",
#         "InterviewDate": "11/02/2022" 
#     }
# }

# internship_id_counter = 2

# @app.route("/internships/")
# def get_tasks():
#     res = {"internships": list(internships.values())}
#     return json.dumps(res), 200

# @app.route("/internships/", methods = ["POST"])
# def create_task():
#     global internship_id_counter
#     body = json.loads(request.data)
#     name = body["CompanyName"]
#     status = body["ApplicationStatus"]
#     date = body["InterviewDate"]
#     internship = {"id": internship_id_counter, "CompanyName": name, "ApplicationStatus": status, "InterviewDate": date}
#     internships[internship_id_counter] = internship
#     internship_id_counter += 1
#     return json.dumps(internship), 201

# @app.route("/internships/<int:internship_id>/")
# def get_internship(internship_id):
#     internship = internships.get(internship_id)
#     if not internship:
#         return json.dumps({"error": "Internship not found"}), 404
#     return json.dumps(internship), 200

# @app.route("/internships/<int:internship_id>/", methods=["POST"])
# def update_internship(internship_id):
#     internship = internships.get(internship_id)
#     if not internship:
#         return json.dumps({"error": "Internship not found"}), 404
#     body = json.loads(request.data)
#     internship["CompanyName"] = body["CompanyName"]
#     internship["ApplicationStatus"] = body["ApplicationStatus"]
#     internship["InterviewDate"] = body["InterviewDate"]
#     return json.dumps(internship), 200

# @app.route("/internships/<int:internship_id>/", methods=["DELETE"])
# def delete_internship(internship_id):
#     internship = internships.get(internship_id)
#     if not internship:
#         return json.dumps({"error": "Internship not found"}), 404
#     del internships[internship_id]
#     return json.dumps(internship), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
