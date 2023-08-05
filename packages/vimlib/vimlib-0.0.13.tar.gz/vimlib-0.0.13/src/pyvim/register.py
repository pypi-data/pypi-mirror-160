""" Interface to Vim's register's.

Currently a placeholder.
"""
try:
    import vim
except ImportError:
    pass


# py3 pyvim.register('*') = pyvim.current.file.name
class Register:
    pass
