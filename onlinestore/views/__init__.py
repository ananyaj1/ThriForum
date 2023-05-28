"""Views, one for each page."""
from onlinestore.views.index import show_index
from onlinestore.views.account import show_login, target, show_create 
from onlinestore.views.account import show_delete, show_edit, show_logout, show_password
from onlinestore.views.user import user
from onlinestore.views.item import show_item
from onlinestore.views.interaction import target_likes