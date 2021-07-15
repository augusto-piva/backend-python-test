import json
from . import db
from .models import Users, Todos
from alayatodo import app
from flask_paginate import (Pagination, get_page_parameter)
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    flash
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Users.query.filter_by(username = username ,password = password).first()
    user_dict = {'id': user.id , 'username': user.username}
    if user:
        session['user'] = user_dict
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todos.query.get(id)
    return render_template('todo.html', todo=todo)

@app.route('/todo/json/<id>', methods=['GET'])
def todo_in_json(id):
    todo = Todos.query.get(id)
    todo_json = json.dumps({'id': todo.id, 'description': todo.description, 'completed':todo.completed})
    return render_template('todo_in_json.html', todo=todo_json)




@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    if not session.get('logged_in'):
        return redirect('/login')
    #Filtro las todos del usuario logeado.
    todos = Todos.query.filter_by(user_id = session.get('user')['id'])
    page = request.args.get(get_page_parameter(), type=int, default=1)
    #Paginacion
    pagination = Pagination(css_framework='foundation', per_page = 4, page = page , total = todos.count(), search=search, record_name = 'todos')
    todos_paginated = todos.paginate(per_page= 4).items
    return render_template('todos.html', todos_paginated =todos_paginated,pagination=pagination)

@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    #Task 1 from here
    if request.form.get('description') == '':
        flash('There must be a description')
        return redirect('/todo')
        #to here
    #Task 4 from here
    try:
        todo = Todos(user_id = session['user']['id'], description = request.form.get('description', '') )
        db.session.add(todo)
        db.session.commit()
        flash("Todo '%s' Succesfully added" % request.form.get('description'))
    except:
        flash("Todo '%s' was not added" % request.form.get('description'))
    #To here
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    #Task 4 from here
    try:
        todo_delete = Todos.query.get(id)
        db.session.delete(todo_delete)
        db.session.commit()
        flash("Todo '%s' Succesfully deleted" % todo_delete.description)
    except:
        flash("Todo '%s' was not deleted" % todo_delete.description)
        #to here
    return redirect('/todo')

@app.route('/todo/completed/<id>', methods=['POST'])
def todo_completed(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo_update = Todos.query.get(id)
    if todo_update.completed == 1:
        todo_update.completed = 0
        db.session.commit()
    else:
        todo_update.completed = 1
        db.session.commit()
    print(todo_update.completed)
    
    return redirect('/todo')   