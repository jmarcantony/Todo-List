from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__) # Initialize main app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db' # Configuire Database
db = SQLAlchemy(app) # Initialize Database
Bootstrap(app) # Initialize Bootstrap

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(80), unique=True, nullable=False)

db.create_all()

# Routes
@app.route("/")
def home():
    todos = Todo.query.all()    
    return render_template("index.html", todos=todos, length=len(todos))


@app.route("/add", methods=["POST"])
def add():
    todo = Todo(todo=request.form["todo"])
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