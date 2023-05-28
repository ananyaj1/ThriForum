"""
Likes and comments interactions
"""
import flask
import onlinestore 



@onlinestore.app.route('/likes/', methods=['POST'])
def target_likes():
    """Doc string."""
    target = flask.request.args.get('target')
    if not target:
        target = '/'
    connection = onlinestore.model.get_db()
    logname = flask.session['logname']
    itemid = flask.request.form.get("itemid")
    # TO DO: how to error check?
    cur = connection.execute(
        "SELECT owner, itemid "
        "FROM likes "
        "WHERE owner = ? AND itemid = ?",
        (logname, itemid, )
    )
    check = cur.fetchone()

    if flask.request.form['operation'] == 'like':
        if check:
            flask.abort(409)
        connection.execute(
            "INSERT INTO likes(owner, itemid) "
            "VALUES(?, ?) ",
            (logname, itemid, )
        )

    if flask.request.form['operation'] == 'unlike':
        if not check:
            flask.abort(409)
        connection.execute(
            "DELETE FROM likes "
            "WHERE owner=? AND itemid=? ",
            (logname, itemid, )
        )
        

    return flask.redirect(target)

@onlinestore.app.route('/comments/', methods=['POST'])
def target_comments():
    """Doc string."""
    target = flask.request.args.get('target')
    if not target:
        target = '/'
    connection = onlinestore.model.get_db()
    logname = flask.session['logname']
    itemid = flask.request.form.get("itemid")
    commentid = flask.request.form.get("commentid")
    text = flask.request.form.get("text")

    if flask.request.form['operation'] == 'create':
        if not text:
            return flask.abort(400)
        connection.execute(
            "INSERT INTO comments(owner, itemid, text) "
            "VALUES(?, ?, ?) ",
            (logname, itemid, text, )
        )

    if flask.request.form['operation'] == 'delete':
        cur = connection.execute(
            "SELECT * "
            "FROM comments "
            "WHERE itemid = ? AND owner = ? ",
            (itemid, logname, )
        )
        if not cur:
            return flask.abort(403)
        connection.execute(
            "DELETE FROM comments "
            "WHERE owner= ? AND commentid = ?",
            (logname, commentid, )
        )
    return flask.redirect(target)
