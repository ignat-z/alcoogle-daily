import operator
from datetime import datetime

import pystache

TEMPLATE = r"""
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Alcoogle</title>
</head>

<body>
  <section>
    <ul>
    {{#heroes}}
        <li>{{name}} - {{count}}</li>
    {{/heroes}}
    </ul>

    Alcoogle - {{today}}
  </section>
</body>
</html>
"""


class ResultsView():
    def __init__(self, today=None):
        self.today = today or datetime.now()

    def render(self, result, template=TEMPLATE):
        heroes = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
        return self.__render_text(template, {
            'heroes': list(map(self.__present_hero, heroes)),
            'today': self.today.strftime('%Y-%m-%d'),
        })

    def __present_hero(self, pair):
        return {'name': pair[0], 'count': pair[1]}

    def __render_text(self, template, ctx):
        return pystache.render(template, ctx)
