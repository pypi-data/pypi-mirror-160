# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""
.. versionadded:: 4.0

Plug-in interfaces for coverage.py.

Coverage.py supports a few different kinds of plug-ins that change its
behavior:

* File tracers implement tracing of non-Python file types.

* Configurers add custom configuration, using Python code to change the
  configuration.

* Dynamic context switchers decide when the dynamic context has changed, for
  example, to record what test function produced the coverage.

To write a coverage.py plug-in, create a module with a subclass of
:class:`~coverage.CoveragePlugin`.  You will override methods in your class to
participate in various aspects of coverage.py's processing.
Different types of plug-ins have to override different methods.

Any plug-in can optionally implement :meth:`~coverage.CoveragePlugin.sys_info`
to provide debugging information about their operation.

Your module must also contain a ``coverage_init`` function that registers an
instance of your plug-in class::

    import coverage

    class MyPlugin(coverage.CoveragePlugin):
        ...

    def coverage_init(reg, options):
        reg.add_file_tracer(MyPlugin())

You use the `reg` parameter passed to your ``coverage_init`` function to
register your plug-in object.  The registration method you call depends on
what kind of plug-in it is.

If your plug-in takes options, the `options` parameter is a dictionary of your
plug-in's options from the coverage.py configuration file.  Use them however
you want to configure your object before registering it.

Coverage.py will store its own information on your plug-in object, using
attributes whose names start with ``_coverage_``.  Don't be startled.

.. warning::
    Plug-ins are imported by coverage.py before it begins measuring code.
    If you write a plugin in your own project, it might import your product
    code before coverage.py can start measuring.  This can result in your
    own code being reported as missing.

    One solution is to put your plugins in your project tree, but not in
    your importable Python package.


.. _file_tracer_plugins:

File Tracers
============

File tracers implement measurement support for non-Python files.  File tracers
implement the :meth:`~coverage.CoveragePlugin.file_tracer` method to claim
files and the :meth:`~coverage.CoveragePlugin.file_reporter` method to report
on those files.

In your ``coverage_init`` function, use the ``add_file_tracer`` method to
register your file tracer.


.. _configurer_plugins:

Configurers
===========

.. versionadded:: 4.5

Configurers modify the configuration of coverage.py during start-up.
Configurers implement the :meth:`~coverage.CoveragePlugin.configure` method to
change the configuration.

In your ``coverage_init`` function, use the ``add_configurer`` method to
register your configurer.


.. _dynamic_context_plugins:

Dynamic Context Switchers
=========================

.. versionadded:: 5.0

Dynamic context switcher plugins implement the
:meth:`~coverage.CoveragePlugin.dynamic_context` method to dynamically compute
the context label for each measured frame.

Computed context labels are useful when you want to group measured data without
modifying the source code.

For example, you could write a plugin that checks `frame.f_code` to inspect
the currently executed method, and set the context label to a fully qualified
method name if it's an instance method of `unittest.TestCase` and the method
name starts with 'test'.  Such a plugin would provide basic coverage grouping
by test and could be used with test runners that have no built-in coveragepy
support.

In your ``coverage_init`` function, use the ``add_dynamic_context`` method to
register your dynamic context switcher.

"""

from . import files


class FileReporter:
    """Support needed for files during the analysis and reporting phases.

    File tracer plug-ins implement a subclass of `FileReporter`, and return
    instances from their :meth:`CoveragePlugin.file_reporter` method.

    There are many methods here, but only :meth:`lines` is required, to provide
    the set of executable lines in the file.

    See :ref:`howitworks` for details of the different coverage.py phases.

    """

    def __init__(self, filename):
        """Simple initialization of a `FileReporter`.

        The `filename` argument is the path to the file being reported.  This
        will be available as the `.filename` attribute on the object.  Other
        method implementations on this base class rely on this attribute.

        """
        self.filename = filename

    def __repr__(self):
        return f"<{self.__class__.__name__} filename={self.filename!r}>"

    def relative_filename(self):
        """Get the relative file name for this file.

        This file path will be displayed in reports.  The default
        implementation will supply the actual project-relative file path.  You
        only need to supply this method if you have an unusual syntax for file
        paths.

        """
        return files.relative_filename(self.filename)

    def source(self):
        """Get the source for the file.

        Returns a Unicode string.

        The base implementation simply reads the `self.filename` file and
        decodes it as UTF8.  Override this method if your file isn't readable
        as a text file, or if you need other encoding support.

        """
        with open(self.filename, "rb") as fin:
            return fin.read().decode("utf8")

    def lines(self):
        """Get the executable lines in this file.

        Your plug-in must determine which lines in the file were possibly
        executable.  This method returns a set of those line numbers.

        Returns a set of line numbers.

        """

    def excluded_lines(self):
        """Get the excluded executable lines in this file.

        Your plug-in can use any method it likes to allow the user to exclude
        executable lines from consideration.

        Returns a set of line numbers.

        The base implementation returns the empty set.

        """
        return set()

    def translate_lines(self, lines):
        """Translate recorded lines into reported lines.

        Some file formats will want to report lines slightly differently than
        they are recorded.  For example, Python records the last line of a
        multi-line statement, but reports are nicer if they mention the first
        line.

        Your plug-in can optionally define this method to perform these kinds
        of adjustment.

        `lines` is a sequence of integers, the recorded line numbers.

        Returns a set of integers, the adjusted line numbers.

        The base implementation returns the numbers unchanged.

        """
        return set(lines)

    def arcs(self):
        """Get the executable arcs in this file.

        To support branch coverage, your plug-in needs to be able to indicate
        possible execution paths, as a set of line number pairs.  Each pair is
        a `(prev, next)` pair indicating that execution can transition from the
        `prev` line number to the `next` line number.

        Returns a set of pairs of line numbers.  The default implementation
        returns an empty set.

        """
        return set()

    def no_branch_lines(self):
        """Get the lines excused from branch coverage in this file.

        Your plug-in can use any method it likes to allow the user to exclude
        lines from consideration of branch coverage.

        Returns a set of line numbers.

        The base implementation returns the empty set.

        """
        return set()

    def translate_arcs(self, arcs):
        """Translate recorded arcs into reported arcs.

        Similar to :meth:`translate_lines`, but for arcs.  `arcs` is a set of
        line number pairs.

        Returns a set of line number pairs.

        The default implementation returns `arcs` unchanged.

        """
        return arcs

    def exit_counts(self):
        """Get a count of exits from that each line.

        To determine which lines are branches, coverage.py looks for lines that
        have more than one exit.  This function creates a dict mapping each
        executable line number to a count of how many exits it has.

        To be honest, this feels wrong, and should be refactored.  Let me know
        if you attempt to implement this method in your plug-in...

        """
        return {}

    def missing_arc_description(self, start, end, executed_arcs=None):     # pylint: disable=unused-argument
        """Provide an English sentence describing a missing arc.

        The `start` and `end` arguments are the line numbers of the missing
        arc. Negative numbers indicate entering or exiting code objects.

        The `executed_arcs` argument is a set of line number pairs, the arcs
        that were executed in this file.

        By default, this simply returns the string "Line {start} didn't jump
        to {end}".

        """
        return f"Line {start} didn't jump to line {end}"

    def source_token_lines(self):
        """Generate a series of tokenized lines, one for each line in `source`.

        These tokens are used for syntax-colored reports.

        Each line is a list of pairs, each pair is a token::

            [('key', 'def'), ('ws', ' '), ('nam', 'hello'), ('op', '('), ... ]

        Each pair has a token class, and the token text.  The token classes
        are:

        * ``'com'``: a comment
        * ``'key'``: a keyword
        * ``'nam'``: a name, or identifier
        * ``'num'``: a number
        * ``'op'``: an operator
        * ``'str'``: a string literal
        * ``'ws'``: some white space
        * ``'txt'``: some other kind of text

        If you concatenate all the token texts, and then join them with
        newlines, you should have your original source back.

        The default implementation simply returns each line tagged as
        ``'txt'``.

        """
        for line in self.source().splitlines():
            yield [('txt', line)]

    # Annoying comparison operators. Py3k wants __lt__ etc, and Py2k needs all
    # of them defined.

    def __eq__(self, other):
        return isinstance(other, FileReporter) and self.filename == other.filename

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.filename < other.filename

    def __le__(self, other):
        return self.filename <= other.filename

    def __gt__(self, other):
        return self.filename > other.filename

    def __ge__(self, other):
        return self.filename >= other.filename

    __hash__ = None     # This object doesn't need to be hashed.
