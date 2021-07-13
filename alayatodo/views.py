import json
from alayatodo import app
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

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
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
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)

@app.route('/todo/json/<id>', methods=['GET'])
def todo_in_json(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = json.dumps(cur.fetchone())
    return render_template('todo_in_json.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


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
        g.db.execute(
        "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
        % (session['user']['id'], request.form.get('description', ''))
        )
        g.db.commit()
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
        cur = g.db.execute("SELECT description FROM todos WHERE id = '%s'" % id)
        g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)    
        g.db.commit()
        flash("Todo '%s' Succesfully deleted" % cur.fetchone()['description'])
    except:
        flash("Todo '%s' was not deleted" % cur.fetchone()['description'])
        #to here
    return redirect('/todo')

@app.route('/todo/completed/<id>', methods=['POST'])
def todo_completed(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("UPDATE todos SET completed = 1 WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')   