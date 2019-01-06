from flask_restful import Resource,request
from flask import Blueprint , session, jsonify
from flaskr.db import get_db

api_bp = Blueprint('api', __name__)
todos = {}

def unauthor():
    return {'error' : 'Please sign in'}, 401


class simpleBlog(Resource):
    def get(self, blog_id):
        db = get_db()
        user_id = session.get('user_id')

        if user_id is None:
            unauthor()
        elif db.execute('SELECT count(*)'
                        ' FROM post'
                        ' WHERE id = ? ', (blog_id,)
                        ).fetchone() is None:
            return {'error': 'Not found'}, 201

        getQuery = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u'
            ' ON p.author_id = u.id '
        ).fetchone()
        # print(getQuery)
        # print(getQuery['username'])
        response = {
            'user': getQuery['username'],
             'title': getQuery['title'],
             'body': getQuery['body']
         }
        return jsonify(response)

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

class blogs(Resource):
    def get(self, todo_id):
        if todos.get(todo_id) is None:
            return {'error': 'Not found'}, 201
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}