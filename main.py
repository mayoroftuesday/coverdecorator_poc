import unittest
from coverdecoratorplugin.decorator import covers

def foo():
    foo_value = 1
    bar()
    return foo_value

def bar():
    bar_value = 2
    return bar_value

class FoobarTestCase(unittest.TestCase):

    @covers('main.foo')
    def test_foo(self):
        result = foo()
        assert result == 1

if __name__ == '__main__':
    unittest.main()

