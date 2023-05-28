import flask
import hashlib
import onlinestore
from flask import request
from onlinestore.api.items import InvalidUsage

@onlinestore.app.route('/api/v1/comments/', methods=['POST'])
def create_comment():
    """Doc string i am lazy."""
    connection = onlinestore.model.get_db()
    if "logname" not in flask.session:
        if flask.request.authorization is None:
            raise InvalidUsage('Not authorized', status_code=403)
        logname = flask.request.authorization['username']
        password = flask.request.authorization['password']
        cur = connection.execute(
            "SELECT username, password "
            "FROM users "
            "WHERE username = ? ",
            (logname, )
        )
        log_pass = cur.fetchall()
        if not log_pass:
            raise InvalidUsage('Not authorized', status_code=403)
        algorithm = log_pass[0]['password'].split('$')[0]
        salt = log_pass[0]['password'].split('$')[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        if log_pass[0]['password'] != password_db_string:
            raise InvalidUsage('Not authorized', status_code=403)
    else:
        logname = flask.session['logname']
    args = request.args
    itemid = args.get('itemid', default=0, type=int)
    if not itemid:
        raise InvalidUsage('itemid not given', status_code=404)
    # need to check that postid is within bounds
    if itemid <= 0:
        raise InvalidUsage('Postid cannot be negative', status_code=404)
    ## COMMENTED OUT CODE IS FOR INFINITE SCROLL, TODO:REIMPLEMENT
    """
    cur = connection.execute(
        "SELECT itemid "
        "FROM items "
        "ORDER BY postid DESC ",
    )
    idcheck = cur.fetchone()
    if idcheck['postid'] < postid:
        raise InvalidUsage('Postid not in bounds', status_code=404)
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        text = request.json['newComment']
    cur = connection.execute(
        "INSERT INTO comments(owner, itemid, text ) "
        "VALUES(?, ?, ?) ",
        (logname, itemid, text),
    )
    # get id of inserted comment
    cur = connection.execute(
        "SELECT last_insert_rowid() "
    )
    commentid = cur.fetchone()
    commentid = commentid['last_insert_rowid()']
    context = {
        "commentid": commentid,
        "lognameOwnsThis": True,
        "owner": logname,
        "ownerShowUrl": "/users/{}/".format(logname),
        "text": text,
        "url": "/api/v1/comments/{}/".format(commentid)
    }
    return flask.jsonify(**context), 201

@onlinestore.app.route('/api/v1/comments/<int:commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Doc string i am lazy."""
    connection = onlinestore.model.get_db()
    if "logname" not in flask.session:
        if flask.request.authorization is None:
            raise InvalidUsage('Not authorized', status_code=403)

        logname = flask.request.authorization['username']
        password = flask.request.authorization['password']
        cur = connection.execute(
            "SELECT username, password "
            "FROM users "
            "WHERE username = ? ",
            (logname, )
        )
        log_pass = cur.fetchall()
        if not log_pass:
            raise InvalidUsage('Not authorized', status_code=403)
        algorithm = log_pass[0]['password'].split('$')[0]
        salt = log_pass[0]['password'].split('$')[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        if log_pass[0]['password'] != password_db_string:
            raise InvalidUsage('Not authorized', status_code=403)
    else:
        logname = flask.session['logname']
    cur = connection.execute(
        "SELECT commentid, owner, itemid "
        "FROM comments "
        "WHERE commentid = ? ",
        (commentid, )
    )
    check = cur.fetchone()
    if not check:
        flask.abort(404)
    if check['owner'] != logname:
        flask.abort(403)
    cur = connection.execute(
        "DELETE from comments "
        "WHERE commentid = ? ",
        (commentid, )
    )
    status_code = flask.Response(status=204)
    return status_code
