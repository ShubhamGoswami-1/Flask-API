from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return '<Task %r>' % self.id
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'date_created': self.date_created
        }

@app.route('/addTask', methods=['POST'])
def index():
    task_content = request.form['content']
    new_task = Todo(content = task_content)

    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Task added successfully',
            'task': {
                'id': new_task.id,
                'content': new_task.content,
                'date_created': new_task.date_created
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'There was an issue adding your task',
            'error': str(e)
        }), 500


@app.route('/getAllTasks', methods=['GET'])
def getAllTasks():
    tasks = Todo.query.order_by(Todo.date_created).all()
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify({
            'status': 'success',
            'message': 'Task added successfully',
            'tasks': tasks_list
    }), 200


@app.route('/updateTask/<int:id>', methods=['PUT'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    task_content = request.form['content']

    try:
        task.content = task_content
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'There was an issue updating your task',
            'error': str(e)
        }), 500


@app.route('/deleteTask/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Task deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'There was an issue deleting your task',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)