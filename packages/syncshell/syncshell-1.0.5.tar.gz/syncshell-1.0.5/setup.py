# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syncshell', 'syncshell.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub==1.55',
 'black==22.3.0',
 'fire==0.1.3',
 'flake8==4.0.1',
 'halo==0.0.12',
 'pytest-testdox>=3.0.1,<4.0.0',
 'pytest==7.1.2']

setup_kwargs = {
    'name': 'syncshell',
    'version': '1.0.5',
    'description': "Keep your machine's shell history synchronized.",
    'long_description': '<h1 align="center">SyncShell</h1>\n\n<div align="center">\n  <strong>Yet another tool for laziness</strong>\n</div>\n<div align="center">\n  Keep your machine\'s shell history synchronized\n</div>\n<br/>\n<div align="center">\n  <!-- Build Status -->\n  <a href="https://github.com/msudgh/syncshell/actions/workflows/test.yaml">\n    <img src="https://github.com/msudgh/syncshell/actions/workflows/test.yaml/badge.svg?branch=main"\n      alt="Build Status" />\n  </a>\n  <!-- License -->\n  <a href="https://mit-license.org/msudgh">\n    <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg"\n      alt="MIT License" />\n  </a>\n  <!-- Release -->\n  <a href="https://github.com/msudgh/syncshell/releases">\n    <img src="https://img.shields.io/github/release/msudgh/syncshell.svg"\n      alt="PyPi" />\n  </a>\n  <!-- PyPi -->\n  <a href="https://pypi.org/project/syncshell/">\n    <img src="https://img.shields.io/pypi/v/syncshell.svg"\n      alt="PyPi" />\n  </a>\n</div>\n<br/>\n\n## Get SyncShell\nCurrently, `SyncShell` is just available on `PyPi` and by the following command install the latest version:\n```bash\n$ pip install syncshell # Maybe sudo need\n```\n```bash\n$ syncshell -- --help\nType:        Application\nString form: <syncshell.cli.Application object at 0x1035f51c0>\nDocstring:   SyncShell CLI Application\n\nUsage:       syncshell \n             syncshell auth\n             syncshell download\n             syncshell upload\n```\n\n## How it Works\nThe actual idea of SyncShell is synchronization of your all device\'s shell history, it means you don\'t need to have concerns when you want to sync your office and home machine\'s shell history. Application integrated and built on top of Github Gist, and written in Python (CLI).\n\nAccording to Github API, you can generate a token key with `gist` scope to access to Gist. \nGists have two **`public`**, **`secret`** type which syncshell while executing `syncshell upload` command will upload your history file and store them on Github Gist securely (**private**).\n\nOn the others machine, by executing `syncshell download` after entering your token key and created Gist ID you can download the gist and sync your shell\'s history.\n\n  > Gists will be secret until you don\'t share it with someone else, In other words, It\'ll be secret and safe until you only have the Github Token and Gist ID.\n\n## Usage\n  > Currently, `SyncShell` just support `zsh` and supporting other shells is in WIP.\n\nBefore SyncShell can be useful you need to setup your Github token key:\n\n  1. Open [**Github personal access tokens**](https://github.com/settings/tokens) page, [**Generate a new token**](https://github.com/settings/tokens/new) with `gist` scope feature.\n  2. Execute the **`syncshell auth`** command, Enter your token key to validate and confirm it.\n  3. Done :wink:\n\nNow you can try to upload your shell history by the following command:\n\n```bash\n$ syncshell upload\n```\n\nAfter the uploading process, you\'ll take a Gist ID that by this ID and your Github token, you can download history on the others machine by executing the following command:\n```bash\n$ syncshell download\n```\n\n## Todo\n- [ ] Write more test cases\n- [x] Support `zsh`, `bash`\n\n## Contributing\nSo nice you wanna contribute to this repository. Thank you. You may contribute in several ways consists of:\n\n* Creating new features\n* Fixing bugs\n\n#### Installing dependencies\n[Poetry Installation](https://python-poetry.org/docs/#installation) is straightforward walkthough to setup a versatile package manager.\n\nBy the following command install syncshell dependencies\n```bash\n# Clone syncshell repository\n$ git clone git@github.com:msudgh/syncshell.git\n$ cd syncshell\n$ poetry install\n```\n\n#### Tests\nBefore submiting your PR, Execute the below command to be sure about passing test cases.\n```bash\n$ poetry run pytest -c pytest.ini -s\n```\n\nDone :wink:\n\n## License\nThe code is licensed under the MIT License. See the data\'s [LICENSE](https://github.com/msudgh/syncshell/blob/main/LICENSE) file for more information.\n',
    'author': 'Masoud Ghorbani',
    'author_email': 'msud.ghorbani@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/msudgh/syncshell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.13,<4.0.0',
}


setup(**setup_kwargs)
