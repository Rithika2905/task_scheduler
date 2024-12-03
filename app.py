from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client=MongoClient('mongodb://localhost:27017/')

db = client.task_scheduler
collections = db.tasks


'''{
    "user_id" : "1",
    "task_name" : "read",
    "created_at" : "2-nov",
    "enddate" : "10-nov",
    "completed" : null
}'''

#res = collections.insert_one(task1)

@app.route("/")
def index():
    return "hello"

@app.route('/tasks', methods=["POST"])
def add_task():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    task ={"user_id" : data.get("user_id"),
           "task_name" : data.get("task_name"),
           "created_at" : data.get("created_at"),
           "enddate" : data.get("enddate"),
           "completed" : data.get("completed",None), 
        }
    result = collections.insert_one(task)

    return jsonify({"message": "added", "task_id":str(result.inserted_id)}),201


@app.route('/tasks', methods=["GET"])
def get_task():
    user_id= request.args.get("user_id")
    query = {"user_id":user_id} if user_id else {}
    tasks = list(collections.find(query))

    for i in tasks:
        i["_id"] = str(i["_id"])
    return jsonify({"tasks":tasks}), 200

@app.route('/tasks/<task_id>', methods=["PUT"])
def update(task_id):
    task_object_id = ObjectId(task_id)
    if not ObjectId.is_valid(task_id):
        return jsonify({"error":"not valid"})
    
    data = request.json
    if not data:
        return jsonify({"error":"not valid"})
    
    result = collections.update_one(
        {"_id":task_object_id},
        {"$set":data}
    )

    if result.matched_count == 0:
        return jsonify({"error":"not valid"})
    
    return jsonify({"success":" valid"})

@app.route('/tasks/<task_id>',methods =["DELETE"])
def delete(task_id):
    task_object_id = ObjectId(task_id)
    if not ObjectId.is_valid(task_id):
        return jsonify({"error":"not valid"})
    result= collections.delete_one({"_id":task_object_id})
    if result.deleted_count == 0:
        return jsonify({"error":"not valid"})
    
    return jsonify({"success":" valid"})

if __name__ == '__main__':
    app.run(debug=True)