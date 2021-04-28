from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def home():
    task_list = Task.query.all()
    return render_template('index.html',task_list=task_list)

@app.route("/add",methods=["POST"])
def add():
    title = request.form.get('title')
    new_task = Task(title=title,complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect (url_for('home'))

@app.route("/update/<int:task_id>")
def update(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect (url_for('home'))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect (url_for('home'))

if __name__ == '__main__':
    db.create_all()
    new_task = Task(title="Task 1",complete=False)
    
    app.run(port=5000,debug=True)