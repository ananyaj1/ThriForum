"""
onlinestore user view.

URLs include:
/
"""
import flask
import onlinestore
import arrow


@onlinestore.app.route('/items/<item_id>/', methods=['GET'])
def show_item(item_id):
    """Display / route."""
    # Connect to database
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session["logname"]
    connection = onlinestore.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT itemid, owner, created AS timestamp, filename "
        "FROM items "
        "WHERE itemid = ? ",
        (item_id, )
    )
    items = cur.fetchone()
    items["timestamp"] = arrow.get(items["timestamp"]).humanize()
    com = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE itemid = ? ",
        (item_id, )
    )
    comments = com.fetchall()
    pro = connection.execute(
        "SELECT filename AS owner_img_url "
        "FROM users "
        "WHERE username = ? ",
        (items['owner'], )
    ) 
    prof = pro.fetchone()
    items["owner_img_url"] = prof['owner_img_url']
    pro = connection.execute(
        "SELECT owner "
        "FROM likes "
        "WHERE itemid = ?",
        (items['itemid'], )
    )
    temp = pro.fetchall()
    count = len(temp)
    lik = [d['owner'] for d in temp]
    if logname in lik:
        items['user_liked'] = True
    else:
        items['user_liked'] = False
    items['likes'] = count

    # Add database info to context
    # users/username, following, comments, likes
    context = {"logname": logname, "items": items, "comments": comments}
    return flask.render_template("item.html", **context)
