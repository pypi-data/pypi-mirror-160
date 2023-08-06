# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pls_cli', 'pls_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.4.4,<13.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pls = pls_cli.please:app']}

setup_kwargs = {
    'name': 'pls-cli',
    'version': '0.2.0',
    'description': '',
    'long_description': '<h1 align="center">\n  💻 PLS-CLI\n</h1>\n<p align="center">\n    <a href="https://github.com/guedesfelipe/pls-cli/actions/workflows/ci.yml" target="_blank">\n        <img src="https://github.com/guedesfelipe/pls-cli/actions/workflows/ci.yml/badge.svg?branch=main" />\n    </a>\n    <a href="https://github.com/guedesfelipe/pls-cli/actions/workflows/security.yml" target="_blank">\n        <img src="https://github.com/guedesfelipe/pls-cli/actions/workflows/security.yml/badge.svg?branch=main" />\n    </a>\n    <a href="https://codecov.io/gh/guedesfelipe/pls-cli" > \n      <img src="https://codecov.io/gh/guedesfelipe/pls-cli/branch/main/graph/badge.svg"/> \n    </a>\n    <a href="https://pypi.org/project/pls-cli/" target="_blank">\n      <img src="https://img.shields.io/pypi/v/pls-cli?label=pypi%20package" />\n    </a>\n    <a href="" target="_blank">\n      <img src="https://img.shields.io/pypi/pyversions/pls-cli.svg?color=green&logo=python&logoColor=yellow" />\n    </a>\n    <img src="https://img.shields.io/badge/platforms-windows%7C%20linux%7C%20macos-lightgrey" />\n</p>\n\n<p align="center">\n  <em>If you are like me, and your terminal is your home, this CLI will make your life better, I hope 😄</em>\n  <br>\n  <br>\n  <img src="https://user-images.githubusercontent.com/25853920/180621358-bf89cd86-2109-41e7-9fea-bbd1a6a56ff4.gif" />\n</p>\n\n# 🛠 Installation\n\n```sh\npip install pls-cli\n```\n\n# ⬆️ Upgrade version\n\n```sh\npip install pls-cli --upgrade\n```\n\n# ⚙️ Configuration\n\nTo run **`pls-cli`** everytime you open your shell\'s:\n\n<details><p><summary>Bash</p></summary>\n\n```sh\necho \'pls\' >> ~/.bashrc\n```\n\n</details>\n\n<details><p><summary>Zsh</p></summary>\n\n```sh\necho \'pls\' >> ~/.zshrc\n```\n\n</details>\n\n<details><p><summary>Fish</p></summary>\n\n```sh\necho \'pls\' >> ~/.config/fish/config.fish\n```\n\n</details>\n\n<details><p><summary>Ion</p></summary>\n  \n```sh\necho \'pls\' >> ~/.config/ion/initrc\n```\n\n</details>\n\n<details><p><summary>Tcsh</p></summary>\n  \n```sh\necho \'pls\' >> ~/.tcshrc\n```\n\n</details>\n\n<details><p><summary>Xonsh</p></summary>\n\n```sh\necho \'pls\' >> ~/.xonshrc\n```\n</details>\n\n<details><p><summary>Powershell</p></summary>\n    \nAdd the following to the end of `Microsoft.PowerShell_profile.ps1`. You can check the location of this file by querying the `$PROFILE` variable in PowerShell. Typically the path is `~\\Documents\\PowerShell\\Microsoft.PowerShell_profile.ps1` or `~/.config/powershell/Microsoft.PowerShell_profile.ps1` on -Nix.\n \n```txt\npls\n```\n\n</details>\n\n# ⌨️ Commands\n\n```sh\npls --help\n```\n\nOr for more inforametion you can see in the [documentation](https://guedesfelipe.github.io/pls-cli/commands).\n\n\n# 🎨 Color Configuration\n\nYou can configure all colors with envs!!\n\n<details><p><summary>Setting env on Linux, macOS, Windows Bash:</p></summary>\n\n```sh\nexport PLS_ERROR_LINE_STYLE="#e56767"\n```\n\n</details>\n\n<details><p><summary>Setting env on Windows PowerShell:</p></summary>\n\n```sh\n$Env:PLS_ERROR_LINE_STYLE = "#e56767"\n```\n\n</details>\n\nAll envs:\n```sh\nexport PLS_ERROR_LINE_STYLE="#e56767"\nexport PLS_ERROR_TEXT_STYLE="#ff0000 bold"\n\nexport PLS_WARNING_LINE_STYLE="#FFBF00"\nexport PLS_WARNING_TEXT_STYLE="#FFBF00 bold"\n\nexport PLS_UPDATE_LINE_STYLE="#61E294"\nexport PLS_UPDATE_TEXT_STYLE="#61E294 bold"\n\nexport PLS_INSERT_DELETE_LINE_STYLE="#bb93f2"\n\nexport PLS_INSERT_DELETE_TEXT_STYLE="#a0a0a0"\n\nexport PLS_MSG_PENDING_STYLE="#61E294"\nexport PLS_TABLE_HEADER_STYLE="#d77dd8"\nexport PLS_TASK_DONE_STYLE="#a0a0a0"\nexport PLS_TASK_PENDING_STYLE="#bb93f2"\nexport PLS_HEADER_GREETINGS_STYLE="#FFBF00"\nexport PLS_QUOTE_STYLE="#a0a0a0"\nexport PLS_AUTHOR_STYLE="#a0a0a0"\n\nexport PLS_BACKGROUND_BAR_STYLE="bar.back"\nexport PLS_COMPLETE_BAR_STYLE="bar.complete"\nexport PLS_FINISHED_BAR_STYLE="bar.done"\n```\n\n<details><p><summary>You can specify the background color like this:</p></summary>\n\n```sh\nexport PLS_QUOTE_STYLE="#a0a0a0 on blue"\n```\n\n</details>\n\nIf you create some theme, share with us <a href="https://github.com/guedesfelipe/pls-cli/discussions/1#discussion-4174647" target="_blank">here</a> ♥️.\n\n## 💄 Formatting a task\n\n<details><p><summary>You can format your tasks with:</p></summary>\n\n```sh\npls add "[b]Bold[/], [i]Italic[/], [s]Strikethrough[/], [d]Dim[/], [r]Reverse[/], [red]Color Red[/], [#FFBF00 on green]Color exa with background[/], :star:, ✨"\n```\n\n![image](https://user-images.githubusercontent.com/25853920/175835339-8059bc7e-0538-4e2d-aed8-80487d7b2478.png)\n\n</details>\n\n## 🚧 TMUX integration\n\nUsing `pls count-done` and `pls count-undone`.\n\n## 🤝 Special thanks\n\n**PLS-CLI** stands on the shoulders of giants:\n\n* <a href="https://github.com/tiangolo/typer" target="_blank">Typer</a> for the CLI tool.\n* <a href="https://github.com/Textualize/rich" target="_blank">Rich</a> for the beautiful formatting in terminal.\n\n---\n\n<p align="center">\n  <a href="https://ko-fi.com/guedesfelipe" target="_blank">\n    <img src="https://user-images.githubusercontent.com/25853920/175832199-6c75d866-31b8-4209-bd1a-db116a6dd032.png" width=300 />\n  </a>\n</p>\n',
    'author': 'Felipe Guedes',
    'author_email': 'contatofelipeguedes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://guedesfelipe.github.io/pls-cli/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
