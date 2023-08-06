try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version('democritus_hypothesis')
except PackageNotFoundError:
    message = 'Unable to find a version number for "democritus_hypothesis". This likely means the library was not installed properly. Please re-install it and, if the problem persists, raise an issue here: https://github.com/democritus-project/democritus-hypothesis/issues.'
    print(message)

__author__ = '''Floyd Hightower'''
__email__ = 'floyd.hightower27@gmail.com'
__version__ = '2021.01.08'

from .hypothesis_wrapper import *
