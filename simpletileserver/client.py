import tempfile
import webbrowser
from jinja2 import Environment, PackageLoader, select_autoescape


def render_map(center, max_zoom):

    env = Environment(
        loader=PackageLoader('simpletileserver', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('map.html')

    html = template.render(x=center[0],
                           y=center[1],
                           max_zoom=max_zoom,
                           zoom=int(max_zoom / 2))

    temp= tempfile.NamedTemporaryFile(delete=False)
    path=temp.name+'.html'

    temp_file = open(path, 'w')
    temp_file.write(html)
    temp_file.close()
    webbrowser.open('file://' + path, new=2)

