from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///daytodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class DayTodo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method =="POST":
        title=request.form['title']
        desc=request.form['desc']
        if title!="" and desc !="":
            daytodo=DayTodo(title=title, desc=desc)
            db.session.add(daytodo)
            db.session.commit()
        else:
            print('emptty fild')
    allTodo=DayTodo.query.all()
    
    return render_template('index.html',allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    Todo=DayTodo.query.filter_by(sno=sno).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method =="POST":
        title=request.form['title']
        desc=request.form['desc']
        Todo=DayTodo.query.filter_by(sno=sno).first()
        Todo.title=title
        Todo.desc=desc
        db.session.add(Todo)
        db.session.commit()
        return redirect('/')
    Todo=DayTodo.query.filter_by(sno=sno).first()
    return render_template('update.html',Todo=Todo)

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == "__main__":
    app.run(debug=True)