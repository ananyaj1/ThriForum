import flask
import hashlib
import onlinestore
from flask import make_response
from onlinestore.api.items import InvalidUsage

@onlinestore.app.route('/api/v1/likes/', methods=['POST'])
def create_like():
    """ this function will add a like to the database """
    connection = onlinestore.model.get_db()
    if "logname" not in flask.session:
        if flask.request.authorization is None:
            raise InvalidUsage('No Enter', status_code=403)
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
            raise InvalidUsage('No Enter', status_code=403)
        algorithm = log_pass[0]['password'].split('$')[0]
        salt = log_pass[0]['password'].split('$')[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        if log_pass[0]['password'] != password_db_string:
            raise InvalidUsage('No Enter', status_code=403)
    else:
        logname = flask.session['logname']
    itemid = flask.request.args.get('itemid', type=int)
    if not itemid:
        raise InvalidUsage('itemid needed', status_code=404)
    # need to check that itemid is within bounds
    if itemid <= 0:
        raise InvalidUsage('itemid cannot be negative', status_code=404)
    
    #cur = connection.execute(
        #"SELECT itemid "
        #"FROM items "
        #"ORDER BY itemid DESC ",
    #)
    #idcheck = cur.fetchone()
    
    #if idcheck['itemid'] < itemid:
        #raise InvalidUsage('itemid not in bounds', status_code=404)

    cur = connection.execute(
        "SELECT itemid, owner, likeid "
        "FROM likes "
        "WHERE itemid = ? AND owner = ? ",
        (itemid, logname, )
    )
    check = cur.fetchone()
    if check:
        context = {
            "likeid": check['likeid'],
            "url":  "/api/v1/likes/{}/".format(check['likeid'])
        }
        return make_response(flask.jsonify(**context), 200)
    cur = connection.execute(
        "INSERT INTO likes(owner, itemid) "
        "VALUES(?, ?) ",
        (logname, itemid, ),
    )
    # get likeid once a like has been created
    # can this third query be cut? feels redundant
    cur = connection.execute(
        "SELECT last_insert_rowid() ",
    )
    likeid = cur.fetchone()
    likeid = likeid['last_insert_rowid()']
    context = {
        "likeid": likeid,
        "url":  "/api/v1/likes/{}/".format(likeid)
    }
    return make_response(flask.jsonify(**context), 201)

@onlinestore.app.route('/api/v1/likes/<int:likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """Doc string i am lazy."""
    connection = onlinestore.model.get_db()
    if "logname" not in flask.session:
        if flask.request.authorization is None:
            raise InvalidUsage('No Enter', status_code=403)

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
            raise InvalidUsage('No Enter', status_code=403)
        algorithm = log_pass[0]['password'].split('$')[0]
        salt = log_pass[0]['password'].split('$')[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        if log_pass[0]['password'] != password_db_string:
            raise InvalidUsage('No Enter', status_code=403)
    else:
        logname = flask.session['logname']

    cur = connection.execute(
        "SELECT itemid, owner, likeid "
        "FROM likes "
        "WHERE likeid = ? ",
        (likeid, )
    )
    check = cur.fetchone()
    if not check:
        flask.abort(404)
    if check['owner'] != logname:
        flask.abort(403)
    cur = connection.execute(
        "DELETE FROM likes "
        "WHERE likeid = ? ",
        (likeid, )
    )
    status_code = flask.Response(status=204)
    return status_code
