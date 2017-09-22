try:
    # Local file is used in production,
    # the file may not exsits when running in ci
    from .local import *
except ImportError:
    pass
