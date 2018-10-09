import unittest


class TestImport(unittest.TestCase):
    def test_import_general(self):
        import jellylamp

    def test_import_version(self):
        from jellylamp import __version__
        print(__version__)


if __name__ == '__main__':
    unittest.main()
