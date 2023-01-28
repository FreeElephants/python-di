import unittest

from src.di import DI, ComponentNotFoundError


class Foo:
    pass


class Bar:
    foo: Foo

    def __init__(self, foo: Foo):
        self.foo = foo


class MyTestCase(unittest.TestCase):
    def test_get_with_instance(self):
        di = DI()
        foo = di.get(Foo)
        self.assertIsInstance(foo, Foo)

    def test_get_without_autowiring(self):
        di = DI()
        di.autowiring = False
        with self.assertRaises(ComponentNotFoundError):
            di.get(Foo)

    def test_init_injection(self):
        di = DI()
        foo = Foo()

        di[Foo] = foo
        bar = di[Bar]

        self.assertEqual(foo, bar.foo)


if __name__ == "__main__":
    unittest.main()
