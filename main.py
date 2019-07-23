import unittest
from coverdecoratorplugin.decorator import covers

def foo():
    """ Foo is a function we want to test """
    foo_value = 1
    bar()
    return foo_value

def bar():
    """ Bar is called by foo, but we don't have a specific unit test that covers bar """
    bar_value = 2
    return bar_value

class FoobarTestCase(unittest.TestCase):

    @covers('main.foo')
    def test_foo(self):
        """ This test only covers foo(), we don't want to count lines executed in bar() """
        result = foo()
        assert result == 1

# Run unit tests
if __name__ == '__main__':
    unittest.main()

