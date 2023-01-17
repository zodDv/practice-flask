from flask import Flask, render_template, url_for, request, redirect, jsonify 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() # Integrates SQLAlchemy with Flask. This handles setting up one or more engines, associating tables and models with specific engines, and cleaning up connections and sessions after each request.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # access to SQL. # app.config reduces application downtime by enabling you to create rules to validate your configuration
db.init_app(app) #This sets default configuration values, then configures the extension on the application and creates the engines for each bind key. Therefore, this must be called after the application has been configured.


class Todo(db.Model): # Create a db model
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # Create a function to return a string when we add something
        return '<Task %r>' % self.id

@app.route('/', methods=["POST", "GET"]) # '/' - URL on which index function will work, represents main page
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task' 

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks) # Use render_remplate method to render indor from file(index.html)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating your task'
    else:
        return render_template('update.html', task=task)


@app.route('/test', methods=['GET'])
def test_api():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return jsonify([
    {
        "id": task.id,
        "content": task.content,
        "completed": task.completed,
        "date_created": task.date_created,
    } for task in tasks
])



if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(debug=True)  # runs local web server 