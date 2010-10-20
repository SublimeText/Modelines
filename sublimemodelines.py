import sublime, sublimeplugin
import re

MODELINE_PREFIX_TPL = "%s\s*(st|sublime): "
DEFAULT_LINE_COMMENT = '#'
MULTIOPT_SEP = '; '
MAX_LINES_TO_CHECK = 50
LINE_LENGTH = 80
MODELINES_REG_SIZE = MAX_LINES_TO_CHECK * LINE_LENGTH
WINDOW_OPT_PREFIX = 'win:'
APP_OPT_PREFIX = 'app:'

def isModeline(view, line):
    return bool(re.match(buildModelinePrefix(view), view.substr(line)))

def genModelines(view):
    topRegEnd = min(MODELINES_REG_SIZE, view.size())
    candidates = view.lines(sublime.Region(0, view.fullLine(topRegEnd).end()))

    # Consider modelines at the end of the buffer too.
    # There might be overlap with the top region, but it doesn't matter because
    # it means the buffer is tiny.
    bottomRegStart = filter(lambda x: x > -1,
                                ((view.size() - MODELINES_REG_SIZE), 0))[0]
    candidates += view.lines(sublime.Region(bottomRegStart, view.size()))

    for modeline in (view.substr(c) for c in candidates if isModeline(view, c)):
        yield modeline

def genExtractRawOpts(modelines):
    for m in modelines:
        opt = m.partition(':')[2].strip()
        if MULTIOPT_SEP in opt:
            for subopt in (s for s in opt.split(MULTIOPT_SEP)):
                yield subopt
        else:
            yield opt

def genModelineOpts(view):
    modelines = genModelines(view)
    for opt in genExtractRawOpts(modelines):
        name, sep, value = opt.partition(' ')
        if name.startswith(APP_OPT_PREFIX):
            yield sublime.options().set, name[len(APP_OPT_PREFIX):], value
        elif name.startswith(WINDOW_OPT_PREFIX):
            yield view.window().options().set, name[len(WINDOW_OPT_PREFIX):], value
        else:
            yield view.options().set, name, value

def getLineCommentCharacter(view):
    commentChar = ""
    try:
        for pair in view.metaInfo("shellVariables", 0):
            if pair["name"] == "TM_COMMENT_START":
                commentChar = pair["value"]
                break
    except TypeError:
        pass

    return commentChar.strip()

def buildModelinePrefix(view):
    lineComment = getLineCommentCharacter(view).lstrip() or DEFAULT_LINE_COMMENT
    return (MODELINE_PREFIX_TPL % lineComment)


class ExecuteSublimeTextModeLinesCommand(sublimeplugin.Plugin):
    """This plugin provides a feature similar to vim modelines.
    Modelines set options local to the view by declaring them in the
    source code file itself.

        Example:
        mysourcecodefile.py
        # sublime: gutter false; app:showMinimap true
        # sublime: autoIndent false

    The top as well as the bottom of the buffer is scanned for modelines.
    MAX_LINES_TO_CHECK * LINE_LENGTH defines the size of the regions to be
    scanned.
    """
    MAX_LINES_TO_CHECK = 50
    LINE_LENGTH = 80

    def onLoad(self, view):
        try:
            for setter, name, value in genModelineOpts(view):
                setter(name, value)
        except ValueError, e:
            sublime.statusMessage("Sublime Modelines: Bad modeline.")
            print "Sublime Modelines plugin -- Bad option detected: %s, %s\n%s" % (name, value)
            print "Check your file's modelines. Keys cannot be empty strings."
