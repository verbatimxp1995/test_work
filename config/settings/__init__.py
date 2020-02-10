try:
    from config.settings.local import *
except ImportError:
    from config.settings.base import *
