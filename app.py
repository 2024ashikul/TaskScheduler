
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tasks = db.Column(db.String(200), nullable = False)
    date = db.Column(db.DateTime, default= datetime.now())
    
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        content = request.form['taskname']
        if content =="":
            return redirect('/error')
        task = Task(tasks=content)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue"
        
    else:
        tasks = Task.query.order_by(Task.date).all()
        taskcount = 0
        for task in tasks:
            taskcount = taskcount + 1
        empty = False
        if not tasks:
            empty=True
        
        return render_template("home.html", tasks = tasks,empty=empty, taskcount = taskcount)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        content = request.form['taskname']
        if content =="":
            return redirect('/error')
        task = Task(tasks=content)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue"
    else:
        return render_template('add.html')
    
        


@app.route('/error')
def error():
    return render_template('error.html')



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    print("THis place was visited by the compiler")
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleteing this item"


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task_to_update = Task.query.get_or_404(id)
    if request.method == 'POST':
        print("he visited here")
        content = request.form['name']
        task_to_update.tasks = content
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an dissure"
    else:
        return render_template('update.html', task_to_update = task_to_update)
    
    

    

    


if __name__ == "__main__":
    app.run(debug=True)
