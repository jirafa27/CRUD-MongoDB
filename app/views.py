import datetime

from flask import render_template, request
from app import app, db
from app.forms import CreateTaskForm, UpdateTaskForm


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/createTask', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        return render_template("create_task.html", form=CreateTaskForm())
    text = request.form['text']
    created = str(datetime.datetime.now())
    db["tasks"].insert_one({'creation_time': created, 'text': text})
    method = 'CREATE'
    return render_template("success.html", method=method, text=text, created=created)


@app.route('/showTasks', methods=['GET'])
def show_tasks():
    dict_of_tasks = {task['creation_time']: task['text'] for task in db['tasks'].find({}, {"_id": 0, "creation_time": 1, "text": 1})}
    return render_template("show_tasks.html", dict_of_tasks=dict_of_tasks)


@app.route('/updateTask', methods=['GET', 'POST'])
def update_task():
    if request.method == 'GET':
        form = UpdateTaskForm()
        form.created.choices = [(task['creation_time']+"~~"+task['text'], task['creation_time']) for task in db['tasks'].find({}, {"_id": 0, "creation_time": 1, "text": 1})]
        form.process()
        return render_template('update_task.html', form=form)
    text = request.form['text']
    created = request.form['created'].split('~~')[0]
    new_values = {"$set": {"text": text}}
    db['tasks'].update_one({'creation_time': created}, new_values)
    # redisCache.set(created, text)
    method = 'UPDATE'
    return render_template('success.html', method=method, text=text, created=created)


@app.route('/deleteTask', methods=['GET', 'POST'])
def delete_task():
    if request.method == 'GET':
        form = UpdateTaskForm()
        form.created.choices = [(task['creation_time'] + "~~" + task['text'], task['creation_time']) for task in
                                db['tasks'].find({}, {"_id": 0, "creation_time": 1, "text": 1})]
        return render_template('delete_task.html', form=form)
    created = request.form['created'].split("~~")[0]
    text = db['tasks'].find_one_and_delete({'creation_time': created})['text']
    method = 'DELETE'
    return render_template('success.html', method=method, text=text, created=created)


@app.route('/deleteAllTasks', methods=['GET', 'POST'])
def delete_all_tasks():
    len = db['tasks'].count_documents({})
    for i in range(len):
        db['tasks'].find_one_and_delete({})
    return render_template('index.html')
