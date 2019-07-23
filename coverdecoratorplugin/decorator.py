"""
Covers Decorator

When a function is decorated with @covers(...), it will write the target function filename and source file line numbers
to a database.

This can be used by the cover decorator plugin to determine which executed lines should be included in the coverage
output.

NOTE:
_dot_lookup and _importer were stolen from Mock
https://github.com/testing-cabal/mock/blob/master/mock/mock.py

"""

import dis


#### Some utilities stolen from Mock ####

def _dot_lookup(thing, comp, import_path):
    try:
        return getattr(thing, comp)
    except AttributeError:
        __import__(import_path)
        return getattr(thing, comp)

def _importer(target):
    components = target.split('.')
    import_path = components.pop(0)
    thing = __import__(import_path)

    for comp in components:
        import_path += ".%s" % comp
        thing = _dot_lookup(thing, comp, import_path)
    return thing


#### Covers Decorator ####

# Reset output file
coverage_output = open(".coverage.include", "w")
coverage_output.close()

def covers(*covers_objects):
    """ Covers decorator
        Usage: Put a list of targets in the @covers decorator of a test function to indicate what pieces of code it is
        intended to test.

        ```
        @covers('my.project.target1', 'my.project.target2')
        def test_function():
            # perform tests that cover target1 and target2
        ```
    """


    def decorator_covers(function):
        """ Generated coverage decorator """

        # Read in the existing database of covered line numbers (inefficient storage method but it works for now)
        included_lines = {}
        try:
            with open(".coverage.include", "r") as current_file:
                lines = current_file.readlines()
                for line in lines:
                    parts = line.split("|")
                    included_lines[parts[0]] = parts[1].strip()
        except IOError as e:
            pass

        # Load in the intended coverage targets of the test function
        for covers_object in covers_objects:
            target = _importer(covers_object)

            # Get the target's source filename and line numbers
            filename = target.__code__.co_filename
            linenumbers = [x[1] for x in dis.findlinestarts(target.__code__)]

            # Add target's covered line numbers to the database
            line_numbers = set([str(x) for x in linenumbers])
            if filename in included_lines:
                line_numbers.update(included_lines[filename].split(','))
            included_lines[filename] = ','.join(line_numbers)

        # Write the database back to file
        with open(".coverage.include", "w") as output_file:
            for output_filename, output_line_numbers in included_lines.items():
                output_file.write('{}|{}\n'.format(output_filename,  output_line_numbers))

        # Return the decorated function unchanged
        return function

    # Return the generated decorator
    return decorator_covers
