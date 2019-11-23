from datetime import datetime
import operator
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

def render(result):
    heroes = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    return render_text({
        'heroes': list(map(present_hero, heroes)),
        'today': datetime.now().strftime('%Y-%m-%d')
    })


def present_hero(pair):
    return {'name': pair[0], 'count': pair[1] }


def render_text(ctx):
    return pystache.render(TEMPLATE, ctx)


VALUES = {
  'today': '2019-11-19',
  'heroes': [
    {'name': 'John', 'count': 3},
    {'name': 'Oleg', 'count': 5},
  ]
}

# print()
# print(render_html())
