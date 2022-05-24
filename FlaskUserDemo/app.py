import uuid, os, hashlib, pymysql
from flask import Flask, request, render_template, redirect, url_for, session, abort, flash, jsonify
app = Flask(__name__)

# Register the setup page and import create_connection()
from utils import create_connection, setup
app.register_blueprint(setup)

#@app.before_request
#def restrict():
#    restricted_pages = [
#        'list_users',
#        'view_user',
#        'edit_user',
#        'delete_user'
#        ]
#    if 'logged_in' not in session and request.endpoint in restricted_pages:
#        flash("You are not logged in.")
#        return redirect('/login')

@app.route('/')
def home():
    return render_template("index.html", isIndex=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        password = request.form['password']
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email = %s AND password = %s"
                values = (
                    request.form['email'],
                    encrypted_password
                )
                cursor.execute(sql, values)
                result = cursor.fetchone()
            if result:
                session['logged_in'] = True
                session['first_name'] = result['first_name']
                session['role'] = result['role']
                #session['id'] = result['id']
                return redirect('/')
            else:
                flash("Invalid username or password.")
                return redirect('/login')
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# TODO: Add a '/register' (add_user) route that uses INSERT
@app.route('/register', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        password = request.form['password']
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        if request.files['avatar'].filename:
            avatar_image = request.files["avatar"]
            ext = os.path.splitext(avatar_image.filename)[1]
            avatar_filename = str(uuid.uuid4())[:8] + ext
            avatar_image.save("static/images/" + avatar_filename)
        else:
            avatar_filename = None

        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO users
                    (first_name, last_name, email, password, avatar)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                    request.form['first_name'],
                    request.form['last_name'],
                    request.form['email'],
                    encrypted_password,
                    avatar_filename
                )
                #try:
                cursor.execute(sql, values)
                connection.commit()
                #except pymysql.err.IntegrityError:
                #    flash('Email has already been taken.')
                #    return redirect('/register')

            #    sql = "SELECT * FROM users WHERE email = %s AND password = %s"
            #    values = (
            #        request.form['email'],
            #        encrypted_password
            #    )
            #    cursor.execute(sql, values)
            #    result = cursor.fetchone()
            #if result:
            #    session['logged_in'] = True
            #    session['first_name'] = result['first_name']
            #    session['role'] = result['role']
            #    session['id'] = result['id']
            #    return redirect('/')

    return render_template('users_add.html')

# TODO: Add a '/dashboard' (list_users) route that uses SELECT
@app.route('/movies')
def list_users():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM movies")
            result = cursor.fetchall()
    return render_template('movies_list.html', result=result)

## TODO: Add a '/profile' (view_user) route that uses SELECT
#@app.route('/view')
#def view_user():
#    with create_connection() as connection:
#        with connection.cursor() as cursor:
#            cursor.execute("SELECT * FROM users WHERE id = %s", request.args['id'])
#            result = cursor.fetchone()
#    return render_template('users_view.html', result=result)

## TODO: Add a '/delete_user' route that uses DELETE
#@app.route('/delete')
#def delete_user():
#    if session['role'] != 'admin' and str(session['id']) != request.args['id']: 
#        flash("You don't have persmission to delete this user")
#        return redirect('/view?id=' + request.args['id'])
#    with create_connection() as connection:
#            with connection.cursor() as cursor:
#                sql = """DELETE FROM users WHERE id = %s"""
#                values = (request.args['id'])
#                cursor.execute(sql, values)
#                connection.commit()
#    return redirect ('/dashboard')
## TODO: Add an '/edit_user' route that uses UPDATE
#@app.route('/edit', methods=['GET', 'POST'])
#def edit_user():
#    if session['role'] != 'admin' and str(session['id']) != request.args['id']: 
#        flash("You don't have persmission to edit this user")
#        return redirect('/view?id=' + request.args['id'])
#    if request.method == 'POST':
#        if request.files['avatar'].filename:
#            avatar_image = request.files["avatar"]
#            ext = os.path.splitext(avatar_image.filename)[1]
#            avatar_filename = str(uuid.uuid4())[:8] + ext
#            avatar_image.save("static/images/" + avatar_filename)
#            if request.form['old_avatar'] != 'None':
#                os.remove("static/images/" + request.form['old_avatar'])
#            elif request.form['old_avatar'] != 'None':
#                avatar_filename = request.form['old_avatar']
#            else:
#                avatar_filename = None

#        with create_connection() as connection:
#            with connection.cursor() as cursor:
#                if request.form['password']:
#                    password = request.form['password']
#                    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
#                    sql = """UPDATE users SET
#                    first_name = %s,
#                    last_name = %s,
#                    email = %s,
#                    password = %s,
#                    avatar = %s
#                    WHERE id = %s"""
#                    values = (
#                        request.form['first_name'], 
#                        request.form['last_name'], 
#                        request.form['email'],
#                        encrypted_password,
#                        avatar_filename,
#                        request.form['id']
#                    )

#                else:
#                    sql = """UPDATE users SET
#                    first_name = %s,
#                    last_name = %s,
#                    email = %s,
#                    avatar = %s
#                    WHERE id = %s"""
#                    values = (
#                        request.form['first_name'], 
#                        request.form['last_name'], 
#                        request.form['email'],
#                        avatar_filename,
#                        request.form['id']
#                        )
#                cursor.execute(sql, values)
#                connection.commit()

#        return redirect(url_for('home'))
#    else:
#        with create_connection() as connection:
#            with connection.cursor() as cursor:
#                sql = "SELECT * FROM users WHERE id = %s"
#                values = (request.args['id'])
#                cursor.execute(sql, values)
#                result = cursor.fetchone()
#        return render_template("users_edit.html", result=result)

#@app.route('/checkemail')
#def check_email():
#    with create_connection() as connection:
#        with connection.cursor() as cursor:
#            sql = "SELECT * FROM users WHERE email = %s"
#            values = (
#                request.args['email']
#            )
#            cursor.execute(sql, values)
#            result = cursor.fetchone()
#    if result:
#        return jsonify({ 'status': 'Error' })
#    else:
#        return jsonify({ 'status': 'OK' })

if __name__ == '__main__':
    import os

    # This is required to allow flashing messages. We will cover this later.
    app.secret_key = os.urandom(32)

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)