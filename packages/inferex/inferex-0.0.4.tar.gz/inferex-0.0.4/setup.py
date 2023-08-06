# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inferex',
 'inferex.api',
 'inferex.decorator',
 'inferex.decorator.inferex',
 'inferex.deployments',
 'inferex.endpoints',
 'inferex.help',
 'inferex.io',
 'inferex.projects',
 'inferex.subapp',
 'inferex.template']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.4,<2.0.0',
 'GitPython>=3.1.27,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'Pygments>=2.12.0,<3.0.0',
 'dirhash>=0.2.1,<0.3.0',
 'humanize>=4.1.0,<5.0.0',
 'pylint>=2.14.1,<3.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.28.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.64.0,<5.0.0',
 'yaspin>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['inferex = inferex.__main__:main']}

setup_kwargs = {
    'name': 'inferex',
    'version': '0.0.4',
    'description': 'Inferex CLI - Init, deploy and manage your projects on Inferex infrastructure',
    'long_description': '# Inferex CLI\n\nDeploy and manage your AI projects on Inferex infrastructure.\n\n[Please see our online documentation for a tutorial.](https://docs.inferex.com/)\n\n## Installation\n\n```bash\npip install inferex\n```\n\nYou can invoke "inferex --help" for a list of commands. Each command may have\nsubcommands, which can be called with "--help" as well.\n\nVersion 0.0.4:\n\n```bash\nUsage: inferex [OPTIONS] COMMAND [ARGS]...\n\n  Init, deploy, and manage your projects with Inferex.\n\nOptions:\n  --version  Display version number.\n  --help     Show this message and exit.\n\nCommands:\n  delete  🗑️ Delete projects, deployments, and endpoints.\n  deploy  🚀 Deploy a project.\n  get     🌎 Get information about Inferex resources.\n  login   🔑 Fetches your API key from the server.\n  logs    🗒️ Get logs from Inferex deployments.\n  reset   ❌ Deletes files created at login\n```\n\n## CLI - Basic usage\n\n1. Create or navigate to the project folder you wish to deploy. You may copy an\n   example project folder from the examples folder ("face_detection",\n   "sentiment_analysis", etc). Each example has inferex.yaml, pipeline.py, and\n   requirements.txt files.\n\n1. Run the "inferex login" command to log in with your inferex account\n   automatically save your token locally.\n\n1. Run "inferex deploy". This will create a tar archive of your project folder\n   and send it to the server for processing.\n\n## Troubleshooting\n\nHaving issues? Try confirming these variables:\n\n- What is your current working directory?\n- What python interpreter is being used (in bash:  \'which python\')?\n- Do you have a token saved locally? Check this folder depending on your OS:\n\n```plaintext\nMac OS X:               ~/Library/Application Support/inferex\nMac OS X (POSIX):       ~/.inferex\nUnix:                   ~/.config/inferex\nUnix (POSIX):           ~/.inferex\nWindows (roaming):      C:\\Users\\<user>\\AppData\\Roaming\\inferex\nWindows (not roaming):  C:\\Users\\<user>\\AppData\\Local\\inferex\n```\n',
    'author': 'Greg',
    'author_email': 'greg@inferex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
