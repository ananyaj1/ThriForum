"""
onlinestore index (main) view.
URLs include:
/
"""
import flask
import onlinestore
import uuid
import hashlib
import pathlib
import os


@onlinestore.app.route('/accounts/login/', methods=['GET'])
def show_login():
    """Doc string."""
    if "logname" in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template("account_login.html")

@onlinestore.app.route('/accounts/', methods=['POST'])
def target():
    """Doc string."""
    target = flask.request.args.get('target')
    connection = onlinestore.model.get_db()
    #breakpoint()
    if flask.request.form['operation'] == 'login':
        username = flask.request.form['username']
        password = flask.request.form['password']
        if not username or not password:
            flask.abort(400)
        curr = connection.execute(
            "SELECT username, password, admin "
            "FROM users "
            "WHERE username = ?",
            (username, )
        )
        us_pass = curr.fetchone()
        if not us_pass:
            flask.abort(403)
        algorithm = us_pass['password'].split('$')[0]
        salt = us_pass['password'].split('$')[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        if us_pass['password'] != password_db_string:
            flask.abort(403)
        else:
            flask.session['logname'] = username
            flask.session['admin'] = us_pass['admin']
        if target:
            return flask.redirect(target)
        return flask.redirect('/')
    
    if flask.request.form['operation'] == 'create':
        fullname = flask.request.form['fullname']
        username = flask.request.form['username']
        email = flask.request.form['email']
        password = flask.request.form['password']
        fileobj = flask.request.files["file"]
        if (not fullname or not username or
                not email or not password or not fileobj):
            flask.abort(400)

        # make sure user does not exist already
        curr = connection.execute(
            "SELECT username "
            "FROM users "
            "WHERE username = ?",
            (username, )
        )
        profile = curr.fetchone()
        if profile:
            flask.abort(409)

        # check that a password is strong
        # 1. password has a special character
        special = set('!@#$%^&*()?')
        if not any((c in special) for c in password):
            flask.abort(409)
        # 2. password has one uppercase character
        upper = set('QWERTYUIOPASDFGHJKLZXCVBNM')
        if not any((u in upper) for u in password):
            flask.abort(409)
        # password checks over 
        
        # upload file to database
        # Unpack flask object
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        # Save to disk
        path = onlinestore.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        filename = uuid_basename

        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        new_pass = "$".join([algorithm, salt, password_hash])
        

        # for now, every new user is default NOT admin. 
        #Implement application to become admin later 
        connection.execute(
            "INSERT INTO users "
            "(username, fullname, email, filename, password, admin) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (username, fullname, email, filename, new_pass, 0))

        flask.session['logname'] = flask.request.form['username']
        return flask.redirect(flask.url_for('show_index'))
    
    if flask.request.form['operation'] == 'delete':
        logname = flask.session['logname']
        admin = flask.session['admin']
        if not logname:
            flask.abort(403)

        # If user is admin, we need to delete their items & profile pic files & data
        # if user is not admin, we just need to delete their profile pic
        # delete item images in static folder, if any

        if admin == 1:

            curr = connection.execute(
                "SELECT filename "
                "FROM items "
                "WHERE owner = ?",
                (logname, )
            )
            items_user = curr.fetchall()
            for item in items_user:
                file_path = os.path.join(
                    onlinestore.app.config["UPLOAD_FOLDER"], item['filename'])

                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # delete item data from items table
            connection.execute(
                "DELETE FROM items "
                "WHERE owner = ?",
                (logname, )
            )
            connection.commit()

        # delete profile pic (admin or not)
        curr = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?",
            (logname, )
        )
        result = curr.fetchone()

        file_path = os.path.join(
                    onlinestore.app.config["UPLOAD_FOLDER"], result['filename'])

        if os.path.exists(file_path):
            os.remove(file_path)

        # delete user from user table 
        connection.execute(
            "DELETE FROM users "
            "WHERE username = ?",
            (logname, )
        )
        connection.commit()
        flask.session.clear()
        return flask.redirect(flask.url_for('show_login'))
    
    if flask.request.form['operation'] == 'edit_account':
        fullname = flask.request.form['fullname']
        email = flask.request.form['email']
        fileobj = flask.request.files["file"]
        logname = flask.session['logname']
        if not logname:
            flask.abort(403)
        if not fullname or not email:
            flask.abort(400)

        # we need to update the email and password
        connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ?"
            "WHERE username = ?",
            (fullname, email, logname)
        )
        connection.commit()

        # update profile pic
        if fileobj:
            curr = connection.execute(
                "SELECT filename "
                "FROM users "
                "WHERE username = ?",
                (logname, )
            )
            result = curr.fetchone()
            file_path = os.path.join(
                        onlinestore.app.config["UPLOAD_FOLDER"],
                        result['filename'])

            if os.path.exists(file_path):
                os.remove(file_path)

            # upload file to database
            # Unpack flask object
            filename = fileobj.filename
            stem = uuid.uuid4().hex
            suffix = pathlib.Path(filename).suffix
            uuid_basename = f"{stem}{suffix}"
            # Save to disk
            path = onlinestore.app.config["UPLOAD_FOLDER"]/uuid_basename
            fileobj.save(path)
            # change database profile picture
            connection.execute(
                "UPDATE users "
                "SET filename = ? "
                "WHERE users.username = ?",
                (uuid_basename, logname)
            )
            connection.commit()
        return flask.redirect(flask.url_for('user', username=logname))
    
@onlinestore.app.route('/accounts/logout/', methods=['POST', 'GET'])
def show_logout():
    """Doc string."""
    if "logname" in flask.session:
        flask.session.pop("logname")
        return flask.redirect(flask.url_for('show_login'))

    return flask.render_template('account_login.html')

@onlinestore.app.route('/accounts/create/', methods=['GET'])
def show_create():
    """Doc string."""
    if "logname" in flask.session:
        return flask.redirect(flask.url_for('show_edit'))
    return flask.render_template("account_create.html")


@onlinestore.app.route('/accounts/delete/', methods=['GET'])
def show_delete():
    """Doc string."""
    if "logname" not in flask.session:
        flask.abort(403)
    return flask.render_template("account_delete.html")


@onlinestore.app.route('/accounts/edit/', methods=['GET'])
def show_edit():
    """Doc string."""
    if "logname" not in flask.session:
        flask.abort(403)
    connection = onlinestore.model.get_db()
    logname = flask.session['logname']
    curr = connection.execute(
            "SELECT fullname, email, filename "
            "FROM users "
            "WHERE username = ?",
            (logname, )
        )
    us_pass = curr.fetchone()
    context = {
        "email": us_pass['email'],
        "fullname": us_pass['fullname'],
        "propic": us_pass['filename']
    }
    return flask.render_template("account_edit.html", **context)


@onlinestore.app.route('/accounts/password/', methods=['GET'])
def show_password():
    """Doc string."""
    if "logname" not in flask.session:
        flask.abort(403)
    logname = flask.session['logname']
    context = {'logname': logname}
    return flask.render_template("account_password.html", **context)