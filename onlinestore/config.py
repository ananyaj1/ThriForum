"""onLINESTORE development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'$\x82\x1a\x0c\xf7OttW\xf6\xae\x16q7\x88\xff\xbf\
xa7\xdb\xa2`\x0c\xf2\xcb'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
ONLINESTORE_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = ONLINESTORE_ROOT/'onlinestore'/'static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/onlinestore.sqlite3
DATABASE_FILENAME = ONLINESTORE_ROOT/'var'/'onlinestore.sqlite3'