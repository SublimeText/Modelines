from typing import Final, List, Optional, Tuple

import sublime, sublime_plugin

from .app.logger import Logger
from .app.logger_settings import updateLoggerSettings
from .app.modeline import Modeline
from .app.settings import Settings


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
	
	#instance: Optional[SublimeModelinesPlugin] = None
	instance = None
	
	def __init__(self):
		super().__init__()
		Logger.debug("EventListener init.")
		SublimeModelinesPlugin.instance = self
	
	def on_load(self, view: sublime.View) -> None:
		Logger.debug("on_load called.")
		if settings.apply_on_load():
			do_modelines(view)
	
	def on_post_save(self, view: sublime.View) -> None:
		Logger.debug("on_post_save called.")
		if settings.apply_on_save():
			do_modelines(view)


# The command name will be `sublime_modelines_apply`.
# See [the rules to get command names](<https://stackoverflow.com/a/63979147>) for more info.
class SublimeModelinesApplyCommand(sublime_plugin.WindowCommand):
	"""Apply modelines in the given view."""
	
	def run(self):
		view = self.window.active_view()
		if view is None: return
		
		do_modelines(view)


def do_modelines(view: sublime.View) -> None:
	Logger.debug("Searching for and applying modelines.")
	
	view.erase_status(PLUGIN_NAME)
	
	nstart = settings.number_of_lines_to_check_from_beginning()
	nend   = settings.number_of_lines_to_check_from_end()
	lines: List[sublime.Region] = []
	if nstart > 0:
		# Grab lines from beginning of view.
		regionEnd = view.text_point(nstart, 0)
		region = sublime.Region(0, regionEnd)
		lines = view.lines(region)
	last_first_lines = lines[-1] if len(lines) > 0 else None
	if nend > 0:
		# Get the last line in the file.
		line = view.line(view.size())
		# Add the last N lines of the file to the lines list.
		for i in range(0, nend):
			# Add the line to the list of lines
			lines.append(line)
			if line.a == 0:
				# We are at the first line; let’s stop there.
				break
			# Move the line to the previous line
			line = view.line(line.a - 1)
			if not last_first_lines is None and line.a < last_first_lines.b:
				# No overlapping lines.
				break
	
	parsers = [parser_id.get_parser_with_data(settings, view) for parser_id in settings.modelines_formats()]
	
	for line in lines:
		line = view.substr(line)
		for (parser, parser_info) in parsers:
			modeline: Optional[Modeline]
			try:
				modeline = parser.parse_line(line, parser_info)
			except Exception as e:
				Logger.warning(f"Got exception while parsing line with parser “{type(parser)}”. Ignoring. (Note: This should not have happened!) exception=“{e}”, line=“{line}”")
				continue
			
			if not modeline is None:
				Logger.debug(f"Found instructions in a line using parser “{type(parser)}”.")
				for instruction in modeline.instructions:
					try:
						Logger.debug(f"-> Applying modeline instruction: {instruction}.")
						instruction.apply(view)
					except Exception as e:
						Logger.warning(f"Got exception while applying modeline instruction. Ignoring. exception=“{e}”, line=“{line}”")
						continue
				
				# We do not continue to the next parser.
				break
