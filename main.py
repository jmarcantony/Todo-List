from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import datetime

app = Flask(__name__) # Initialize main app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db' # Configuire Database
db = SQLAlchemy(app) # Initialize Database
Bootstrap(app) # Initialize Bootstrap

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.String(80), unique=False, nullable=False)

db.create_all()

# Routes
@app.route("/")
def home():
    todos = Todo.query.all()    
    return render_template("index.html", todos=todos, length=len(todos))


@app.route("/add", methods=["POST"])
def add():
    date = datetime.date.today()
    time = datetime.datetime.now().strftime("%H:%M")
    todo = Todo(todo=request.form["todo"], date=date, time=time)
    db.session.add(todo)
    db.session.commit()
    
    return redirect(url_for('home'))


@app.route("/remove", methods=["POST"])
def remove():
    todo = Todo.query.filter_by(todo=request.form["todo"]).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

    """
        Stay healthy 😎 
        Upgrade Todo List and add more features 🐱‍💻 
        Study for Final Exam 
        Fix Remove button placement 
        Consume Vitamin C 🍊 
        Complete Biology SE Project by tomorrow night! 
    """