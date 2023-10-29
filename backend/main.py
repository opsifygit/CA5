from flask import Flask,request,jsonify,render_template
import os
from pymongo import MongoClient

client = MongoClient("mongo:27017")

# creating a db
db = client["todoList"]

# create a collection
todo_collection = db["todo"]

# a todo document will have title,description and completed fields

app = Flask(__name__)

@app.route("/createTodo",methods=['POST'])
def create_todo():
    title = request.form.get("title")
    description = request.form.get("description")
    completed = request.form.get("completed")

    todoId = todo_collection.insert_one({
        "title":title,
        "description":description,
        "completed":completed
    })

    return jsonify({
        "id":str(todoId),
        "title":title,
        "description":description,
        "completed":completed
    })

@app.route("/updateTodo",methods=['POST'])
def update_todo():
    id = request.json["id"]
    title = request.json["title"]
    description = request.json["description"]
    completed = request.json["completed"]

    todo_collection.update_one({
        "_id":id
    },{
        "$set":{
            "title":title,
            "description":description,
            "completed":completed
        }
    })

    return jsonify({
        "message":"Todo Updated"
    })


@app.route("/deleteTodo",methods=['DELETE'])
def delete_todo():
    id = request.json["id"]

    todo_collection.delete_one({
        "_id":id
    })

    return jsonify({
        "message":"Todo Deleted"
    })

@app.route("/getTodo",methods=['GET'])
def get_All_todo():
    all_todos = todo_collection.find()

    todo_list = []

    for todo in all_todos:
        todo_list.append({
            "id":str(todo["_id"]),
            "title":todo["title"],
            "description":todo["description"],
            "completed":todo["completed"]
        })

    return jsonify(todo_list)

@app.route('/getTodo/<string:id>',methods=['GET'])
def get_todo():
    todo = todo_collection.find_one({
        "_id":id
    })

    return jsonify({
        "id":str(todo["_id"]),
        "title":todo["title"],
        "description":todo["description"],
        "completed":todo["completed"]
    })

@app.route('/',methods=['GET'])
def displayPage():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 8080), debug=True)