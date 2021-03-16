from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import datetime

app = Flask(__name__) # Initialize main app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db' # Configuire Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS' ] = False
db = SQLAlchemy(app) # Initialize Database
Bootstrap(app) # Initialize Bootstrap

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.String(80), unique=False, nullable=False)
    ip = db.Column(db.String(80), nullable=False)

db.create_all()

# Routes
@app.route("/")
def home():
    todos = Todo.query.filter_by(ip=request.remote_addr).all()    
    return render_template("index.html", todos=todos, length=len(todos))


@app.route("/add", methods=["POST"])
def add():
    date = datetime.date.today()
    time = datetime.datetime.now().strftime("%H:%M")
    todo = Todo(todo=request.form["todo"], date=date, time=time, ip=request.remote_addr)
    db.session.add(todo)
    db.session.commit()
    
    return redirect(url_for('home'))


@app.route("/remove", methods=["POST"])
def remove():
    todo = Todo.query.filter_by(todo=request.form["todo"]).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        if request.remote_addr == "127.0.0.1":
            all_todos = {}
            for todo in Todo.query.all():
                all_todos[todo.ip] = []
            for todo in Todo.query.all():
                all_todos[todo.ip].append(todo.todo)
            return render_template("admin.html", todos=all_todos)
        else:
            return render_template("admin_login.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
