"""
Online store's index (main) view.

URLs include:
/
"""
import flask
import onlinestore
import arrow

@onlinestore.app.route('/')
def show_index():
    """Display / route."""
    """
    random change for pull request
    """
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    logname = flask.session['logname']
    connection = onlinestore.model.get_db()
    #logname = flask.session['logname']
    cur = connection.execute(
            "SELECT * "
            "FROM items",
        )
    items = cur.fetchall()
    for item in items: 
        # get user profile pic based on owner of post
        pur = connection.execute(
                    "SELECT filename "
                    "FROM users "
                    "WHERE username = ?",
                    (item['owner'], )
                )
        item['owner_img_url'] = pur.fetchone()['filename']
        # get all comments relating to this post 
        cur = connection.execute(
                    "SELECT * "
                    "FROM comments "
                    "WHERE itemid = ?",
                    (item['itemid'], )
        )
        item['created'] = arrow.get(item['created']).humanize()
        item['comments'] = cur.fetchall()
        # get number of likes, and whether the logged in user
        # has liked the item or not
        lur = connection.execute(
                    "SELECT owner "
                    "FROM likes "
                    "WHERE itemid = ?",
                    (item['itemid'], )
                )
        temp = lur.fetchall()
        count = len(temp)
        l = [d['owner'] for d in temp]
        item['user_liked'] = logname in l
        item['likes'] = count 
    context = { "items": items, "logname": logname}
    return flask.render_template("index.html", **context)