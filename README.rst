Sublime Modelines
=================

Set settings local to a single buffer. A more granular approach to settings
than the per file type ``.sublime-settings`` files.

Inspired in Vim's modelines feature.

Getting Started
***************

Download the `latest release`_ and install it (double-click).

.. _latest release: https://bitbucket.org/guillermooo/sublimemodelines/downloads/SublimeModelines.sublime-package

Side effects
************

Buffers will be scanned ``on_load()`` for modelines and settings will be set
accordingly. Settings will apply **only** to the buffer declaring them.

.. **Note**: Application- and Window-level options declared in modelines are
.. obviously global.

Usage
*****

How to Declare Modelines
------------------------

Modelines must be declared at the top or the bottom of source code files with
one of the following syntaxes::

    # sublime: optionName value
    # sublime: optionName value; anotherOption value; thirdOption value

**Note**: ``#`` is the default comment character. Use the corresponding
single-line comment character for your language. When there isn't a concept of
comment, the default comment character must be used.

.. Application and Window options
.. ------------------------------
.. 
.. To set Application and Window options, prefix the option name with ``app:`` or ``win:``.
.. 
.. Examples
.. ********
.. ::
.. 
..     # sublime: drawWhiteSpace all
..     # sublime: gutter false
..     # sublime: translateTabsToSpaces false
..     # sublime: font Comic Sans 8
..     # sublime: drawWhiteSpace select; wordSeparators &%$·/;?!; translateTabsToSpaces true
..     # sublime: app:showMinimap true


Caveats
*******

If the option's value contains a semicolon (``;``), make sure it isn't followed
by a blank space. Otherwise it will be interpreted as a multioption separator.