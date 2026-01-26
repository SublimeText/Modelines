from importlib import reload
import sublime, sublime_plugin

from . import app

from .app.logger import Logger
from .app.settings import Settings



class SublimeModelinesPlugin(sublime_plugin.EventListener):
	"""
	This plugin provides a feature similar to vim modelines,
	which allow setting options local to the view by declaring them in the source code file itself.
	
	A special token is searched in the source code, which declares a modeline (see later for more info about the token).
	
	The top as well as the bottom of the buffer is scanned for modelines
	(`MAX_LINES_TO_CHECK * LINE_LENGTH` defines the size of the regions to be scanned).
	
	For example, at the end or the beginning of a Python source file, one may find:
	```python
	# sublime: gutter false; translate_tab_to_spaces true
	```
	
	Token formats:
	
	- `^<CommentChar>\\s*(sublime|st):\\s*key1\\s+val1(\\s*;\\s*keyn\\s+valn)\\s*;?`
	- `.{1,7}~~\\s(sublime|st):\\s*key1\\s+val1(\\s*;\\s*keyn\\s+valn)\\s*;?\\s*~~`
	
	The first format works well if you do not change the syntax of the file.
	If you do it is recommended to use the second format
	(because the “comment char” is unknown and will thus default to `#`, which may not work for the syntax you need).
	
	The second format assumes the comment marker (beginning of the line) will have between 1 and 7 characters.
	
	Also the first format does not really work with `/**/`-style comments as the trailing `*/` will be parsed if it is on the same line as the `/*`.
	
	All the keys are guaranteed to never have any space, so there are never any ambiguities parsing them.
	For the values, to have a semicolon inside, you can escape it by doubling it.
	Having a space in the value is ok, except at the beginning or the end, because they will be trimmed.
	(It is _not_ possible at all to have a value with one or more spaces at the beginning or the end.)
	
	When using the second format, values cannot contain a `~~` either.
	
	Examples:
	
	- `# sublime: key1 value1; key2  value with space ; key3 hello;;semicolon!;;; key4 last one;`
	-> `["key1": "value1", "key2": "value with space", "key3": "hello;semicolon!;" "key4": "last one"]`
	- `/*~~ sublime: key1 hello;;semicolon and~~tilde key2 is this parsed? */`
	-> `["key1": "hello;semicolon and"]`
	"""
	
	def __init__(self):
		super().__init__()
		Logger.log_to_tmp = False
		Logger.enable_debug_log = True
		Logger.debug("Plugin init.")
	
	def on_load(self, view):
		pass
		Logger.debug("on_load called.")
		#self.do_modelines(view)
	
	def on_post_save(self, view):
		pass
		Logger.debug("on_post_save called.")
		#self.do_modelines(view)
