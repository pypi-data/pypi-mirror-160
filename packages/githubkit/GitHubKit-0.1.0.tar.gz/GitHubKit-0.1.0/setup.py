# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['githubkit', 'githubkit.rest']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'pydantic>=1.9.1,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'githubkit',
    'version': '0.1.0',
    'description': 'GitHub SDK for Python',
    'long_description': '<!-- markdownlint-disable MD033 MD041 -->\n<div align="center">\n\n[![githubkit](https://socialify.git.ci/yanyongyu/githubkit/image?description=1&descriptionEditable=%E2%9C%A8%20GitHub%20SDK%20for%20Python%20%E2%9C%A8&font=Bitter&language=1&pattern=Circuit%20Board&theme=Light)](https://github.com/yanyongyu/githubkit)\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/yanyongyu/githubkit/master/LICENSE">\n    <img src="https://img.shields.io/github/license/yanyongyu/githubkit" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/githubkit">\n    <img src="https://img.shields.io/pypi/v/githubkit" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">\n  <a href="https://results.pre-commit.ci/latest/github/yanyongyu/githubkit/master">\n    <img src="https://results.pre-commit.ci/badge/github/yanyongyu/githubkit/master.svg" alt="pre-commit" />\n  </a>\n</p>\n\n<div align="center">\n\n<!-- markdownlint-capture -->\n<!-- markdownlint-disable MD036 -->\n\n_✨ The modern, all-batteries-included GitHub SDK for Python ✨_\n\n_✨ Support both **sync** and **async** calls, **fully typed** ✨_\n\n_✨ Always up to date, like octokit ✨_\n\n<!-- markdownlint-restore -->\n\n</div>\n\n## Installation\n\n```bash\npip install githubkit\n# or, use poetry\npoetry add githubkit\n# or, use pdm\npdm add githubkit\n```\n\n## Usage\n\n### Initialization\n\nInitialize a github client using PAT (Token):\n\n```python\nfrom githubkit import GitHub, TokenAuthStrategy\n\ngithub = GitHub("<your_token_here>")\n# or, use TokenAuthStrategy\ngithub = GitHub(TokenAuthStrategy("<your_token_here>"))\n```\n\nor using basic authentication:\n\n```python\nfrom githubkit import GitHub, BasicAuthStrategy\n\ngithub = GitHub(BasicAuthStrategy("<client_id_here>", "<client_secret_here>"))\n```\n\n### Call Rest API\n\n> APIs are fully typed. Typing in the following examples is just for reference only.\n\nSimple sync call:\n\n```python\nfrom githubkit import Response\nfrom githubkit.rest import FullRepository\n\nresp: Response[FullRepository] = github.rest.repos.get(owner="owner", repo="repo")\nrepo: FullRepository = resp.parsed_data\n```\n\nSimple async call:\n\n```python\nfrom githubkit import Response\nfrom githubkit.rest import FullRepository\n\nresp: Response[FullRepository] = await github.rest.repos.async_get(owner="owner", repo="repo")\nrepo: FullRepository = resp.parsed_data\n```\n\nCall API with context (reusing client):\n\n```python\nfrom githubkit import Response\nfrom githubkit.rest import FullRepository\n\n# with GitHub("<your_token_here>") as github:\nwith github:\n    resp: Response[FullRepository] = github.rest.repos.get(owner="owner", repo="repo")\n    repo: FullRepository = resp.parsed_data\n```\n\n```python\nfrom githubkit import Response\nfrom githubkit.rest import FullRepository\n\n# async with GitHub("<your_token_here>") as github:\nasync with github:\n    resp: Response[FullRepository] = await github.rest.repos.async_get(owner="owner", repo="repo")\n    repo: FullRepository = resp.parsed_data\n```\n\n> **Warning**\n>\n> Making sync calls in async context or making async calls in sync context will raise an error.\n\n### Pagination\n\n```python\nfrom githubkit.rest import Issue\n\nfor issue in github.paginate(\n    github.rest.issues.list_for_repo, owner="owner", repo="repo", state="open"\n):\n    issue: Issue\n    print(issue.number)\n```\n\n```python\nfrom githubkit.rest import Issue\n\nasync for issue in github.paginate(\n    github.rest.issues.async_list_for_repo, owner="owner", repo="repo", state="open"\n):\n    issue: Issue\n    print(issue.number)\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yyy@yyydl.top',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yanyongyu/githubkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
