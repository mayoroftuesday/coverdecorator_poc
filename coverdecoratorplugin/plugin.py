import coverage
import inspect

class CoverDecoratorPlugin(coverage.plugin.CoveragePlugin):

    def file_tracer(self, filename):
        return CoverDecoratorTracer(filename)

    def file_reporter(self, filename):
        return CoverDecoratorReporter(filename)

class CoverDecoratorReporter(coverage.python.PythonFileReporter):

    class FakeCoverage(coverage.Coverage):

        def _exclude_regex(self, which):
            return None

    def __init__(self, *args, **kwargs):

        kwargs['coverage'] = self.FakeCoverage()
        super(CoverDecoratorReporter, self).__init__(*args, **kwargs)

class CoverDecoratorTracer(coverage.plugin.FileTracer):

    def __init__(self, filename):
        self.filename = filename

    def source_filename(self):
        return self.filename

    def line_number_range(self, frame):
        print("------------------------------------")
        #frame_info = inspect.getframeinfo(frame)
        #if frame_info.function == 'foo':
        #    outer_frames = inspect.getouterframes(frame)
        #    for outer_frame in outer_frames:
        #        print("FRAME {}\n{}\n".format(i, outer_frames[i]))

        lineno = frame.f_lineno
        return lineno, lineno
