import coverage

class CoverDecoratorPlugin(coverage.plugin.CoveragePlugin):
    """ Cover Decorator plugin for coverage.py
        This plugin takes over coverage calculation for Python files
        Instead of counting all executed lines, it will only count executed lines that are specifically marked
        as being covered by a test function using the @covers decorator
    """

    def file_tracer(self, filename):
        return CoverDecoratorTracer(filename)

    def file_reporter(self, filename):
        return CoverDecoratorReporter(filename)

class CoverDecoratorReporter(coverage.python.PythonFileReporter):
    """ Custom reporter based on PythonFileReporter
        Can't use PythonFileReporter by itself because it causes an error when loading _exclude_regex
    """

    class FakeCoverage(coverage.Coverage):
        """ Avoid the issue with _exclude_regex for now by creating a fake Coverage object that just returns
            None for _exclude_regex
        """

        def _exclude_regex(self, which):
            return None

    def __init__(self, *args, **kwargs):
        """ Replace the coverage paramter when creating the reporter """
        kwargs['coverage'] = self.FakeCoverage()
        super(CoverDecoratorReporter, self).__init__(*args, **kwargs)

class CoverDecoratorTracer(coverage.plugin.FileTracer):
    """ Custom tracer that only counts lines included by the @covers decorator """

    included_line_numbers = []

    def __init__(self, filename):
        self.filename = filename

        # Read in the database created by the @covers decorator and determine if there are any included lines
        # for this file
        with open(".coverage.include") as included_lines:
            for line in included_lines.readlines():
                parts = line.split("|")
                filename = parts[0]
                if filename == self.filename:
                    self.included_line_numbers = [int(lineno) for lineno in parts[1].strip().split(",")]
                    print(self.included_line_numbers)

    def source_filename(self):
        """ Required implementation """
        return self.filename

    def line_number_range(self, frame):
        """ Only report line numbers if they are in the include list """
        lineno = frame.f_lineno

        if lineno in self.included_line_numbers:
            return lineno, lineno
        else:
            return -1, -1
