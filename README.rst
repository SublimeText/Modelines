Sublime Modelines
=================

Set settings local to a single buffer. A more granular approach to settings
than the per file type ``.sublime-settings`` files.

Inspired in Vim's modelines feature.

Getting Started
***************

Download and install `SublimeModelines`_.

See the `installation instructions`_ for ``.sublime-package``\ s.

.. _installation instructions: http://sublimetext.info/docs/en/extensibility/packages.html#installation-of-packages
.. _SublimeModelines: https://bitbucket.org/guillermooo/sublimemodelines/downloads/SublimeModelines.sublime-package

Side Effects
************

Buffers will be scanned ``.on_load()`` for modelines and settings will be set
accordingly. Settings will apply **only** to the buffer declaring them.

.. **Note**: Application- and Window-level options declared in modelines are
.. obviously global.

Usage
*****

How to Declare Modelines
------------------------

Modelines must be declared at the top or the bottom of source code files with
one of the following syntaxes::

    # sublime: option_name value
    # sublime: option_name value; another_option value; third_option value

**Note**: ``#`` is the default comment character. Use the corresponding
single-line comment character for your language. When there isn't a concept of
comment, the default comment character must be used.

Vim compatibility
-----------------

Also following modelines are supported::

    # vim:ai:et:ts=4:
    # sublime: set color_scheme="Packages/Color Scheme - Default/Monokai.tmTheme":
    # sublime: set ignored_packages+=['Vintage']:

.. note:: Modeline values are interpreted as JSON, or string as fallback.  If you 
   use JSON Objects in modeline (like ``[]`` or ``{}``), you can only use this as
   last value in a line, for quick and easy parsing reasons.

There is full vim-modeline-compatibility implemented.  Only some options are
mapped to Sublime Text options.  Following options are supported so far:

- autoindent, ai
- tabstop, ts
- expandtab, et
- syntax, syn
- number, nu

(these are the ones, I used most)

How to Define Comment Characters in Sublime Text
------------------------------------------------

SublimeModelines finds the appropriate single-line comment character by inspecting
the ``shellVariables`` preference, which must be defined in a ``.tmPreferences``
file. To see an example of how this is done, open ``Packages/Python/Miscellaneous.tmPreferences``.

Many packages giving support for programming languages already include this, but
you might need to create a ``.tmPreferences`` file for the language you're working
with if you want SublimeModelines to be available.


Caveats
*******

If the option's value contains a semicolon (``;``), make sure it isn't followed
by a blank space. Otherwise it will be interpreted as a multioption separator.


Non-Standard Options
********************

For some common cases, no directly settable option exists (for example, a
setting to specify a syntax). For such cases, Sublime Modelines provides
non-standard accessors as a stop-gap solution.

**x_syntax** *Packages/Foo/Foo.tmLanguage*

Sets the syntax to the specified *.tmLanguage* file.


Contributers
------------

Kay-Uwe (Kiwi) Lorenz <kiwi@franka.dyndns.org> (http://quelltexter.org)
	- added VIM compatibility
	- smart syntax matching
	- modelines also parsed on save
	- settings are erased from view, if removed from modeline
