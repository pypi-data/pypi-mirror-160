# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graphviz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nr.io.graphviz',
    'version': '0.1.0',
    'description': '',
    'long_description': '# nr.io.graphviz\n\nA simple utility for writing Graphviz files.\n\n## API\n\n*class* __`nr.io.graphviz.writer.GraphvizWriter(out: TextIO, indent: str = "\\t")`__\n\n*function* __`nr.io.graphviz.render.render(graphviz_code: str, format: str, algorithm: str = "dot") -> bytes`__\n\n*function* __`nr.io.graphviz.render.render(graphviz_code: str, format: str, algorithm: str = "dot", output_file: Path) -> None`__\n',
    'author': 'Unknown',
    'author_email': 'me@unknown.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
