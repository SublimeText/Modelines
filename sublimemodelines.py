import sublime, sublimeplugin
import re

SUBLIMETEXT_MODELINE_PREFIX_TPL = "%s\s*(st|sublime): "
DEFAULT_LINE_COMMENT = "#"

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
    return (SUBLIMETEXT_MODELINE_PREFIX_TPL % lineComment)


class ExecuteSublimeTextModeLinesCommand(sublimeplugin.Plugin):
    """
    This plugin provides a feature similar to vim modelines.
    Modelines set options local to the view by declaring them in the
    source code file itself.

        Example:
        mysourcecodefile.py
        # st: gutter false
        # st: autoIndent false

    Note that only the range spanning from 0 to MAX_LINES_TO_CHECK * LINE_LENGTH
    are searched for modelines.

    TODO: let user declare multiple options per line.
    TODO: let user declare modelines in block comments
    """
    MAX_LINES_TO_CHECK = 50
    LINE_LENGTH = 80

    def _getCandidatesTop(self, view):
        endBoundary = min(self.MAX_LINES_TO_CHECK *
                                            self.LINE_LENGTH, view.size())
        # TODO: use lines() here instead.
        candidates = view.lines(sublime.Region(0,
                                            view.fullLine(endBoundary).end()))

        return candidates

    def _getCandidatesBottom(self, view, topCandidatesEnd):

        candidates = []
        # Add region at bottom of file if the file is large enough.
        if topCandidatesEnd + 1 < view.size():

            bottomRegion = sublime.Region(topCandidatesEnd + 1, view.size())
            candidates = view.lines(bottomRegion)

        return candidates

    def _getModelines(self, view):

        candidates = self._getCandidatesTop(view)
        candidates += self._getCandidatesBottom(view, candidates[-1].end())

        return [candidate for candidate in candidates
                                            if self.isModeline(view, candidate)]

    def isModeline(self, view, regionLine):

        if regionLine.empty(): return False

        actualPrefix = buildModelinePrefix(view)

        candidateString = view.substr(regionLine)
        if re.match(actualPrefix, candidateString):
            return True

    def _extractOption(self, view, modeline):

        actualPrefix = buildModelinePrefix(view)

        modelineStr = view.substr(modeline)
        name, discard, value = modelineStr.partition(":")[2].lstrip().partition(" ")

        # spaces in option are illegal in sublime text
        return (name.strip(), value)

    def onLoad(self, view):

        options = [self._extractOption(view, modeline)
                                    for modeline in self._getModelines(view)]

        try:
            for name, value in options:
                view.options().set(name, value)
        except ValueError, e:
            print "Sublime Modelines plugin -- Bad option detected: %s, %s\n%s" % (name, value)
            print "Check your file's modelines. Keys cannot be empty strings."