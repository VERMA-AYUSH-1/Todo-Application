from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy # used for database
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.now())
    
    def __repr__(self): # this is used to print what you want to see of this object like tittle dekha hai description dekhna hai 
        return f"{self.sno} - {self.title}"

    # now for using our database to create we use terminal from app import db
        


@app.route('/',methods=["GET","POST"]) 
def hello_world():
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form["desc"]
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo= Todo.query.all()
    # to render templates we use this
    return render_template("index.html",alltodo=alltodo)
@app.route('/show') # by this we can create routes of different pages like blogs , code etc
def show():
    alltodo= Todo.query.all()
    print(alltodo) 
    return 'This is my production page'
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form["desc"]
        uptodo= Todo.query.filter_by(sno=sno).first()
        uptodo.title=title
        uptodo.desc=desc
        db.session.add(uptodo)
        db.session.commit()
        return redirect("/")
    uptodo= Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",uptodo=uptodo)
@app.route('/delete/<int:sno>')
def delete(sno):
    deltodo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(deltodo)
    db.session.commit()
    return redirect("/")


if __name__=="__main__":
    # app.run(debug=True) 
    app.run(debug=True,port=8000)  # by this we can change the post name