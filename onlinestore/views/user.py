"""
onlinestore user view.

URLs include:
"""
import flask
import onlinestore


@onlinestore.app.route('/users/<username>/')
def user(username):
    """Display / route."""
    # Connect to database
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session["logname"]
    connection = onlinestore.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username == ?",
        (username, )
    )
    users = cur.fetchone()
    
    pos = connection.execute(
        "SELECT * "
        "FROM items "
        "WHERE owner == ?",
        (username, )
    )
    items = pos.fetchall()
    total_items = len(items)

    if items: 
        # if there are items, get comments and likes
        for item in items:
            com = connection.execute(
                "SELECT * "
                "FROM comments "
                "WHERE itemid = ? ",
                (item['itemid'], )
            )
            comments = com.fetchall()
            item['comments'] = comments
            com = connection.execute(
                "SELECT * "
                "FROM likes "
                "WHERE itemid = ? ",
                (item['itemid'], )
            )
            likes = com.fetchall()
            item['likes'] = likes
    # Add database info to context
    # users/username, following, comments, likes
    context = {
        "logname": logname,
        "users": users,
        "total_items": total_items,
        "items": items}
    return flask.render_template("user.html", **context)