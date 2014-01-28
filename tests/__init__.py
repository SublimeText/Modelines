from imp import reload

from . import test_modelines
reload(test_modelines)

from .. import sublime_modelines
reload(sublime_modelines)

from .test_modelines import *

