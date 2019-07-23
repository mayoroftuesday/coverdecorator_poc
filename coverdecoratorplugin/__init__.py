from .plugin import CoverDecoratorPlugin

def coverage_init(reg, options):
    reg.add_file_tracer(CoverDecoratorPlugin())
