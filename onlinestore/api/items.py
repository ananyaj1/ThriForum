"""REST API for items."""
import flask
import hashlib
import onlinestore
from flask import jsonify 


class InvalidUsage(Exception):
    """Doc string i am lazy."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Doc string i am lazy."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Doc string i am lazy."""
        r_v = dict(self.payload or ())
        r_v['message'] = self.message
        r_v['status_code'] = self.status_code
        return r_v


@onlinestore.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Doc string i am lazy."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@onlinestore.app.route('/api/v1/items/<int:itemid_url_slug>/')
def get_item(itemid_url_slug):
    """Return item on itemid.
    """
    connection = onlinestore.model.get_db()
    if "logname" not in flask.session:
        if flask.request.authorization is None:
            raise InvalidUsage('No', status_code=403)

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
            raise InvalidUsage('No', status_code=403)
        algorithm = log_pass[0]['password'].split('$')[0]
        salt = log_pass[0]['password'].split('$')[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        if log_pass[0]['password'] != password_db_string:
            raise InvalidUsage('No', status_code=403)
    else:
        logname = flask.session['logname']
    # need to check that itemid is within bounds
    if itemid_url_slug <= 0:
        raise InvalidUsage('itemid cannot be negative', status_code=404)
    
    cur = connection.execute(
          "SELECT * "
          "FROM items "
          "WHERE itemid = ? ",
          (itemid_url_slug, )
    )
    item = cur.fetchone()
    if not item:
        raise InvalidUsage('Item does not exist', status_code=404)
    # get the filename/image of the owner
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (item['owner'], )
      )
    itemowner = cur.fetchone()
    if not itemowner:
        raise InvalidUsage('Owner image not found', status_code=404)
    
    # COMMENTS INFO FROM DATABASE
    cur = connection.execute(
        "SELECT commentid, owner, text "
        "FROM comments "
        "WHERE itemid = ? ",
        (itemid_url_slug, )
    )
    comments = cur.fetchall()
    for c_o in comments:
        if c_o['owner'] == logname:
            c_o['lognameOwnsThis'] = True
        else:
            c_o['lognameOwnsThis'] = False
        c_o['ownerShowUrl'] = "/users/{}/".format(c_o['owner'])
        c_o['url'] = "/api/v1/comments/{}/".format(c_o['commentid'])
   #### LIKES INFO FROM DATABASE ####
    cur = connection.execute(
          "SELECT likeid, owner "
          "FROM likes "
          "WHERE itemid = ? ",
          (itemid_url_slug, )
    )
    likes = cur.fetchall()
    logname_likes_this = False
    lid = 0
    for like in likes:
        if like['owner'] == logname:
            logname_likes_this = True
            lid = like['likeid']
    like_url = None
    if logname_likes_this:
        like_url = "/api/v1/likes/{}/".format(lid)
    
    context = {
      "comments": comments,
      "comments_url": "/api/v1/comments/?itemid={}".format(itemid_url_slug),
      "created": item['created'],
      "available": item['available'],
      "imgUrl": "static/{}".format(item['filename']),
      "name": item['name'],
      "likes": {
        "lognameLikesThis": logname_likes_this,
        "numLikes": len(likes),
        "url": like_url,
      },
      "owner": item['owner'],
      "ownerImgUrl": "/static/{}".format(itemowner['filename']),
      "ownerShowUrl": "/users/{}/".format(item['owner']),
      "itemShowUrl": "/items/{}/".format(itemid_url_slug),
      "itemid": itemid_url_slug,
      "url": flask.request.path,
      }
    return flask.jsonify(**context)

@onlinestore.app.route('/api/v1/posts/')
def get_certain_posts():
    """Doc string i am lazy."""
    connection = onlinestore.model.get_db()
    if "logname" not in flask.session:
        if flask.request.authorization is None:
            raise InvalidUsage('No', status_code=403)

        else:
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
                raise InvalidUsage('No', status_code=403)
            algorithm = log_pass[0]['password'].split('$')[0]
            salt = log_pass[0]['password'].split('$')[1]
            hash_obj = hashlib.new(algorithm)
            password_salted = salt + password
            hash_obj.update(password_salted.encode('utf-8'))
            password_hash = hash_obj.hexdigest()
            password_db_string = "$".join([algorithm, salt, password_hash])
            if log_pass[0]['password'] != password_db_string:
                raise InvalidUsage('No', status_code=403)
    else:
        logname = flask.session['logname']


    cur = connection.execute(
        "SELECT itemid "
        "FROM items "
    )
    ids = cur.fetchall()

    # populate next string
    # str(ids[0]['postid'])
    # populate results
    results = []
    for i in ids:
        i['url'] = '/api/v1/items/' + str(i['itemid']) + '/'
        results.append(i)
    
    cu_rl = flask.request.path
    # cUrl = flask.request.url.replace('http://localhost', '')
    context = {
      "results": results,
      "logname": logname,
      "url": cu_rl
    }
    return flask.jsonify(**context)
