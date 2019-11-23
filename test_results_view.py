import datetime
import unittest

from results_view import ResultsView


class TestRender(unittest.TestCase):

    def test_render(self):
        result = {"oleg": 5, "ivan": 6}
        template = "{{#heroes}}{{name}},{{count}}:{{/heroes}}{{today}}"
        date = datetime.date(2010, 1, 1)

        self.assertEqual("ivan,6:oleg,5:2010-01-01",
                         ResultsView(date).render(result, template))


if __name__ == '__main__':
    unittest.main()
