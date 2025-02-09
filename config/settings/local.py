from .base import *

# django debug toolbar
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

if DEBUG:
    import mimetypes
    mimetypes.add_type("text/javascript", ".js", True)

