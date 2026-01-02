from .base import *

# Para desenvolvimento, importa configurações específicas
try:
    from .dev import *
except ImportError:
    pass