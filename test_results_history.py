import os
import unittest

from results_history import ResultsHistory


class TestResultsHistory(unittest.TestCase):
    def test_save(self):
        path = './__test__result'
        ResultsHistory(path).save({'key': 'value'})

        self.assertTrue(os.path.isfile(path))

        file = open(path, 'r')
        self.assertEqual('{"key": "value"}', file.read())
        file.close()

        os.remove(path)


if __name__ == '__main__':
    unittest.main()
