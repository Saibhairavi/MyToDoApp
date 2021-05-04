from flask import Flask,request,redirect,render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
db=SQLAlchemy(app)


#-----db creation begins-----
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text)
    done=db.Column(db.Boolean,default=False)

    def __init__(self,content):
        self.content=content
        self.done=False

    def __repr__(self):
        return f'{self.content}'

db.create_all()

#----db is creted--------now
#app
@app.route('/')
def task_list():
    tasks=Task.query.all()
    
    return render_template('list.html',tasks=tasks)

@app.route('/task',methods=['POST'])
def add_tasks():
    content=request.form['content']
    # if not content:
    #     return 'Error!'
    task=Task(content)
    # print(type(task))
    # print(task)
    db.session.add(task)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task=Task.query.get(task_id)
    if not task:
        return redirect('/')
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task=Task.query.get(task_id)
    # print(task,task.done)
    if not task:
        return redirect('/')
    print(task.done)
    if task.done:
        task.done=False
    else:
        task.done=True
    print(task.done)
    db.session.commit()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)