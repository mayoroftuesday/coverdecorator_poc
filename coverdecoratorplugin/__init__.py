from .plugin import CoverDecoratorPlugin

# Register the cover decorator with coverage.py
def coverage_init(reg, options):
    reg.add_file_tracer(CoverDecoratorPlugin())
