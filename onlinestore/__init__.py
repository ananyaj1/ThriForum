"""Online store package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name
app.config['DEBUG'] = True

# Read settings from config module (onlinestore/config.py)
app.config.from_object('onlinestore.config')

# Overlay settings read from a Python file whose path is set in the environment
# variable _SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# $ export _SETTINGS=secret_key_config.py
app.config.from_envvar('ONLINESTORE_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import onlinestore.api  # noqa: E402  pylint: disable=wrong-import-position
import onlinestore.views  # noqa: E402  pylint: disable=wrong-import-position
import onlinestore.model  # noqa: E402  pylint: disable=wrong-import-position