# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versions']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0', 'typing-extensions>=4.3.0']

setup_kwargs = {
    'name': 'versions',
    'version': '1.0.0a1',
    'description': 'Parsing, inspecting and specifying versions.',
    'long_description': '# `versions`\n\n[![License][License Badge]][License]\n[![Version][Version Badge]][Package]\n[![Downloads][Downloads Badge]][Package]\n[![Discord][Discord Badge]][Discord]\n\n[![Documentation][Documentation Badge]][Documentation]\n[![Check][Check Badge]][Actions]\n[![Test][Test Badge]][Actions]\n[![Coverage][Coverage Badge]][Coverage]\n\n> *Parsing, inspecting and specifying versions.*\n\n## Installing\n\n**Python 3.7 or above is required.**\n\n### pip\n\nInstalling the library with `pip` is quite simple:\n\n```console\n$ pip install versions\n```\n\nAlternatively, the library can be installed from source:\n\n```console\n$ git clone https://github.com/nekitdev/versions.git\n$ cd versions\n$ python -m pip install .\n```\n\n### poetry\n\nYou can add `versions` as a dependency with the following command:\n\n```console\n$ poetry add versions\n```\n\nOr by directly specifying it in the configuration like so:\n\n```toml\n[tool.poetry.dependencies]\nversions = "^1.0.0-alpha.1"\n```\n\nAlternatively, you can add it directly from the source:\n\n```toml\n[tool.poetry.dependencies.versions]\ngit = "https://github.com/nekitdev/versions.git"\n```\n\n## Examples\n\n### Versions\n\n[`parse_version`][versions.functions.parse_version] is used to parse versions:\n\n```python\nfrom versions import parse_version\n\nversion = parse_version("1.0.0-dev.1+build.1")\n\nprint(version)  # 1.0.0-dev.1+build.1\n```\n\n### Segments\n\nAll version segments can be fetched with their respective names:\n\n```python\n>>> print(version.release)\n1.0.0\n>>> version.release.parts\n(1, 0, 0)\n>>> print(version.dev)\ndev.1\n>>> (version.dev.phase, version.dev.value)\n("dev", 1)\n>>> print(version.local)\nbuild.1\n>>> version.local.parts\n("build", 1)\n```\n\n### Comparison\n\nVersions support total ordering:\n\n```python\n>>> v1 = parse_version("1.0.0")\n>>> v2 = parse_version("2.0.0")\n>>> v1 == v2\nFalse\n>>> v1 != v2\nTrue\n>>> v1 >= v2\nFalse\n>>> v1 <= v2\nTrue\n>>> v1 > v2\nFalse\n>>> v1 < v2\nTrue\n```\n\n### Specification\n\n`versions` also supports specifying version requirements and matching version against them:\n\nSince versions support total ordering, they can be checked using version sets\n(via [`parse_version_set`][versions.functions.parse_version_set]):\n\n```python\n>>> from versions import parse_version, parse_version_set\n>>> version_set = parse_version_set("^1.0.0")\n>>> version_set\n<VersionRange (>= 1.0.0, < 2.0.0)>\n>>> version = parse_version("1.3.0")\n>>> version\n<Version (1.3.0)>\n>>> version.matches(version_set)\nTrue\n>>> another = parse_version("2.2.0")\n>>> another.matches(version_set)\nFalse\n```\n\n## Documentation\n\nYou can find the documentation [here][Documentation].\n\n## Support\n\nIf you need support with the library, you can send an [email][Email]\nor refer to the official [Discord server][Discord].\n\n## Changelog\n\nYou can find the changelog [here][Changelog].\n\n## Security Policy\n\nYou can find the Security Policy of `versions` [here][Security].\n\n## Contributing\n\nIf you are interested in contributing to `versions`, make sure to take a look at the\n[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].\n\n## License\n\n`versions` is licensed under the MIT License terms. See [License][License] for details.\n\n[Email]: mailto:support@nekit.dev\n\n[Discord]: https://nekit.dev/discord\n\n[Actions]: https://github.com/nekitdev/versions/actions\n\n[Changelog]: https://github.com/nekitdev/versions/blob/main/CHANGELOG.md\n[Code of Conduct]: https://github.com/nekitdev/versions/blob/main/CODE_OF_CONDUCT.md\n[Contributing Guide]: https://github.com/nekitdev/versions/blob/main/CONTRIBUTING.md\n[Security]: https://github.com/nekitdev/versions/blob/main/SECURITY.md\n\n[License]: https://github.com/nekitdev/versions/blob/main/LICENSE\n\n[Package]: https://pypi.org/project/versions\n[Coverage]: https://codecov.io/gh/nekitdev/versions\n[Documentation]: https://nekitdev.github.io/versions\n\n[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2\n[License Badge]: https://img.shields.io/pypi/l/versions\n[Version Badge]: https://img.shields.io/pypi/v/versions\n[Downloads Badge]: https://img.shields.io/pypi/dm/versions\n\n[Documentation Badge]: https://github.com/nekitdev/versions/workflows/docs/badge.svg\n[Check Badge]: https://github.com/nekitdev/versions/workflows/check/badge.svg\n[Test Badge]: https://github.com/nekitdev/versions/workflows/test/badge.svg\n[Coverage Badge]: https://codecov.io/gh/nekitdev/versions/branch/main/graph/badge.svg\n\n[versions.functions.parse_version]: https://nekitdev.github.io/versions/reference#wraps.parse_version\n[versions.functions.parse_version_set]: https://nekitdev.github.io/versions/reference#wraps.parse_version_set\n',
    'author': 'nekitdev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nekitdev/versions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
