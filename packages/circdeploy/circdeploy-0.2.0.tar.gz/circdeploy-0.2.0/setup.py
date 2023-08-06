# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['circdeploy']

package_data = \
{'': ['*']}

install_requires = \
['circup>=1.1.2,<2.0.0',
 'igittigitt>=2.1.2,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['circdeploy = circdeploy.main:main']}

setup_kwargs = {
    'name': 'circdeploy',
    'version': '0.2.0',
    'description': 'Easily deploy your CircuitPython projects',
    'long_description': "# circdeploy\n\n## Easily deploy your CircuitPython projects\n\nDeploys the current working directory to a connected CircuitPython device.\n\nI don't like editing CircuitPython files directly from the mounted device folder. The OS may be\ncreating hidden files or your IDE may be saving files frequently which may trigger the device\nto reboot.\n\n**Default behavior:** Copies all `./**/*.py` and `./**/*.pyc` files from the current directory to an\nautomatically detected CircuitPython device, skipping any files in `.gitignore`. Any remaining\n`./**/*.py` and `./**/*.pyc` files on the device are deleted (`./lib/*` is not deleted)\n\n```text\n$ circdeploy --help\n\n Usage: circdeploy [OPTIONS]\n\n Deploy current CircuitPython project\n All .py and .pyc files in the current directory tree will be copied to the destination (device)\n All other .py and .pyc files in the destination directory tree (device) will be deleted except /lib/\n\n╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --source,--src        -s                    TEXT  Deploy from this location. [default: (current working directory)]                     │\n│ --destination,--dest  -d                    TEXT  Deploy to this location. [default: (device path automatically detected)]              │\n│ --delete                  --no-delete             Delete files in destination. [default: delete]                                        │\n│ --use-gitignore           --no-gitignore          Ignore files using .gitignore files relative to source path. [default: use-gitignore] │\n│ --dry-run                                         Don't copy files, only output what would be done.                                     │\n│ --install-completion                              Install completion for the current shell.                                             │\n│ --show-completion                                 Show completion for the current shell, to copy it or customize the installation.      │\n│ --help                                            Show this message and exit.                                                           │\n╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n",
    'author': 'Patrick Seal',
    'author_email': 'code@plasticrake.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/plasticrake/circdeploy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
