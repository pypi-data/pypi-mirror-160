# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anitui', 'anitui.utils', 'anitui.widgets']

package_data = \
{'': ['*'],
 'anitui': ['script/README.md',
            'script/README.md',
            'script/README.md',
            'script/README.md',
            'script/package-lock.json',
            'script/package-lock.json',
            'script/package-lock.json',
            'script/package-lock.json',
            'script/package.json',
            'script/package.json',
            'script/package.json',
            'script/package.json',
            'script/run.sh',
            'script/run.sh',
            'script/run.sh',
            'script/run.sh',
            'script/src/*',
            'script/src/api/*',
            'script/src/api/auth/*',
            'script/src/tests/*',
            'script/src/utils/*']}

install_requires = \
['commonmark>=0.9.1,<0.10.0',
 'pygments-arm>=0.7.5,<0.8.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'textual>=0.1.18,<0.2.0']

entry_points = \
{'console_scripts': ['anitui = anitui.__init__:main']}

setup_kwargs = {
    'name': 'anitui',
    'version': '0.1.4',
    'description': 'A TUI to browse Anime',
    'long_description': '# ani-tui\n\nTUI written in Python using [Textual](https://github.com/Textualize/textual) to navigate local Anime files. \n\n## Getting Started\n\n### Install\n\nTo use ani-tui simply install the Python package:\n\nUnix\n```bash\npip3 install anitui\n```\n\nWindows\n```powershell\npy -m pip install anitui\n```\n\nThe TUI can then be run by simply typing `anitui` in the shell.\n\n### Development Setup\n\nPackage management and deployment is done with [poetry](https://python-poetry.org/). To setup the repository for development:\n\n1. Clone the Git repository\n\n```bash\ngit clone https://github.com/cakoshakib/ani-tui\n```\n\n2. Install the Python packages\n\n```bash\npoetry install\n```\n\n3. Run the TUI\n\n```bash\npoetry run anitui\n```\n\n## Notes\n\nStill in development, expect bugs! :)\n\n## License\nMIT\n\n',
    'author': 'cakoshakib',
    'author_email': 'cakoshakib@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cakoshakib/ani-tui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
