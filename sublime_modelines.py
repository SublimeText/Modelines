import sublime, sublime_plugin
import re

MODELINE_PREFIX_TPL = "%s\s*(st|sublime): "
DEFAULT_LINE_COMMENT = '#'
MULTIOPT_SEP = '; '
MAX_LINES_TO_CHECK = 50
LINE_LENGTH = 80
MODELINES_REG_SIZE = MAX_LINES_TO_CHECK * LINE_LENGTH
WINDOW_OPT_PREFIX = 'win:'
APP_OPT_PREFIX = 'app:'

def is_modeline(view, line):
    return bool(re.match(build_modeline_prefix(view), view.substr(line)))

def gen_modelines(view):
    topRegEnd = min(MODELINES_REG_SIZE, view.size())
    candidates = view.lines(sublime.Region(0, view.full_line(topRegEnd).end()))

    # Consider modelines at the end of the buffer too.
    # There might be overlap with the top region, but it doesn't matter because
    # it means the buffer is tiny.
    bottomRegStart = filter(lambda x: x > -1,
                                ((view.size() - MODELINES_REG_SIZE), 0))[0]
    candidates += view.lines(sublime.Region(bottomRegStart, view.size()))

    for modeline in (view.substr(c) for c in candidates if is_modeline(view, c)):
        yield modeline

def gen_raw_options(modelines):
    for m in modelines:
        opt = m.partition(':')[2].strip()
        if MULTIOPT_SEP in opt:
            for subopt in (s for s in opt.split(MULTIOPT_SEP)):
                yield subopt
        else:
            yield opt

def gen_modeline_options(view):
    modelines = gen_modelines(view)
    for opt in gen_raw_options(modelines):
        name, sep, value = opt.partition(' ')
        if name.startswith(APP_OPT_PREFIX):
            # yield sublime.settings().set, name[len(APP_OPT_PREFIX):], value
            pass
        elif name.startswith(WINDOW_OPT_PREFIX):
            # yield view.window().settings().set, name[len(WINDOW_OPT_PREFIX):], value
            pass
        else:
            yield view.settings().set, name, value

def get_line_comment_char(view):
    commentChar = ""
    try:
        for pair in view.meta_info("shellVariables", 0):
            if pair["name"] == "TM_COMMENT_START":
                commentChar = pair["value"]
                break
    except TypeError:
        pass

    return commentChar.strip()

def build_modeline_prefix(view):
    lineComment = get_line_comment_char(view).lstrip() or DEFAULT_LINE_COMMENT
    return (MODELINE_PREFIX_TPL % lineComment)


def to_json_type(v):
    """"Convert string value to proper JSON type.
    """
    if v.lower() in ("false", "true"):
        v = (True if v == "true" else False)
    elif v.isdigit():
        v = int(v)
    elif v.replace(".").isdigit():
        v = float(v)
    # ...
    return v


class ExecuteSublimeTextModeLinesCommand(sublime_plugin.EventListener):
    """This plugin provides a feature similar to vim modelines.
    Modelines set options local to the view by declaring them in the
    source code file itself.

        Example:
        mysourcecodefile.py
        # sublime: gutter false
        # sublime: translate_tab_to_spaces true

    The top as well as the bottom of the buffer is scanned for modelines.
    MAX_LINES_TO_CHECK * LINE_LENGTH defines the size of the regions to be
    scanned.
    """
    def on_load(self, view):
        try:
            for setter, name, value in gen_modeline_options(view):
                setter, name, value
                setter(name, to_json_type(value))
                print type(to_json_type(value))
        except ValueError, e:
            sublime.status_message("SublimeModelines: Bad modeline detected.")
            print "SublimeModelines: Bad option detected: %s, %s\n%s" % (name, value)
            print "SublimeModelines: Tip: Keys cannot be empty strings."
