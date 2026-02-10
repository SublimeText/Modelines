from typing import Final, Optional

import sublime, sublime_plugin

from .app.logger import Logger
from .app.settings import Settings
from .app.logger_settings import updateLoggerSettings


# The plugin structure is heavily inspired by <https://github.com/pestilence669/VimModelines/blob/b7d499b705277a1aa8ee1dd6387f78b734a8512c/vimmodelines.py>.
# We have mostly added typing, and fixed a potential issue if on_load or on_post_save is called in a view which is not the front-most one in a window.


PLUGIN_NAME: Final[str] = "SublimeModelines"

# Before everything else, update the settings of the logger.
settings = Settings()
updateLoggerSettings(settings)


def plugin_loaded():
	Logger.debug("Plugin loaded.")
	
	# Call on_load() for existing views, since files may load before the plugin.
	# First we verify the plugin is properly instantiated (it should be).
	plugin = SublimeModelinesPlugin.instance
	if plugin is None:
		Logger.warning("Plugin instance is not set.")
		return
	
	for w in sublime.windows():
		for g in range(w.num_groups()):
			view = w.active_view_in_group(g)
			if view is None: continue
			plugin.on_load(view)


def plugin_unloaded():
	Logger.debug("Plugin unloaded.")


class SublimeModelinesPlugin(sublime_plugin.EventListener):
	"""Event listener to invoke the command on load & save."""
	
	instance: Optional[SublimeModelinesPlugin] = None
	
	def __init__(self):
		super().__init__()
		Logger.debug("EventListener init.")
		SublimeModelinesPlugin.instance = self
	
	def on_load(self, view: sublime.View) -> None:
		Logger.debug("on_load called.")
		if settings.apply_on_load:
			do_modelines(view)
	
	def on_post_save(self, view: sublime.View) -> None:
		Logger.debug("on_post_save called.")
		if settings.apply_on_save:
			do_modelines(view)


# The command name will be `sublime_modelines_apply`.
# See [the rules to get command names](<https://stackoverflow.com/a/63979147>) for more info.
class SublimeModelinesApplyCommand(sublime_plugin.WindowCommand):
	"""Apply modelines in the given view."""
	
	def run(self):
		view = self.window.active_view()
		if view is None or view.is_scratch():
			return
		
		do_modelines(view)


def do_modelines(view: sublime.View) -> None:
	Logger.debug("Searching for and applying modelines.")
	
	view.erase_status(PLUGIN_NAME)
