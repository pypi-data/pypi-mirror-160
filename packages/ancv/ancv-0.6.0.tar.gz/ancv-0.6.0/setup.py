# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ancv',
 'ancv.data',
 'ancv.data.models',
 'ancv.utils',
 'ancv.visualization',
 'ancv.web']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0',
 'cachetools>=5.2.0,<6.0.0',
 'gidgethub>=5.1.0,<6.0.0',
 'humanize>=4.1.0,<5.0.0',
 'pydantic[email]>=1.9.1,<2.0.0',
 'rich>=12.4.4,<13.0.0',
 'structlog>=21.5.0,<22.0.0',
 'typer>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'ancv',
    'version': '0.6.0',
    'description': "Render 'JSON Resume' sources to ANSI-enriched output for terminal clients (cURL, wget, ...) to consume.",
    'long_description': "# ancv\n\nGetting you [an CV](https://www.youtube.com/watch?v=mJUtMEJdvqM) (ANSI-v?) straight to your terminal.\n\nBe warned though, this is entirely useless:\n\n![Users Venn diagram](docs/images/users-venn.svg)\n\n## Getting started\n\n1. Create a resume according to the [JSON Resume Schema](https://jsonresume.org/schema/) ([schema specification](https://github.com/jsonresume/resume-schema/blob/master/schema.json)) either:\n\n   - manually,\n   - exporting from LinkedIn using [Joshua Tzucker's LinkedIn exporter](https://joshuatz.com/projects/web-stuff/linkedin-profile-to-json-resume-exporter/) ([repo](https://github.com/joshuatz/linkedin-to-jsonresume)), or\n   - exporting from one of the platforms advertised as offering [JSON resume integration](https://jsonresume.org/schema/):\n     - <https://gitconnected.com/portfolio-api>\n     - <https://represent.io/>\n     - <https://www.doyoubuzz.com/us/>\n2. [Create a gist](https://gist.github.com/) named `resume.json` with those resume contents.\n   See [here](https://gist.github.com/thomasdavis/c9dcfa1b37dec07fb2ee7f36d7278105) for a working example from a [JSON Resume co-founder](https://github.com/orgs/jsonresume/people).\n3. Try it out!\n\n   ```bash\n   curl -L ancv.io/username\n   ```\n\n## Design\n\n### Features\n\nThis being a hobby project, new (and old) features were tried out and used:\n\n- fully async using [`aiohttp`](https://docs.aiohttp.org/en/stable/) and [gidgethub](https://gidgethub.readthedocs.io/en/latest/index.html)\n- ~~[structural pattern matching](https://peps.python.org/pep-0634/), introduced in Python 3.10~~ Not used since [unsupported by AWS lambda](https://github.com/aws/aws-lambda-base-images/issues/31) (2022-07-16)\n- [fully typed](https://mypy.readthedocs.io/en/stable/index.html) using Python type hints, verified through `mypy --strict` (with additional, [even stricter settings](pyproject.toml))\n- [structural logging](https://github.com/hynek/structlog) with a JSON event stream output\n- [`pydantic`](https://pydantic-docs.helpmanual.io/) for fully typed data validation (e.g., for APIs), facilitated by [automatic `pydantic` model generation](https://koxudaxi.github.io/datamodel-code-generator/) from e.g. OpenAPI specs like [GitHub's](https://github.com/github/rest-api-description/tree/main/descriptions/api.github.com) or [JSON Resume's](https://github.com/jsonresume/resume-schema/blob/master/schema.json), allowing full support from `mypy` and the IDE when using said validated data\n- [12 Factor App](https://12factor.net/) conformance:\n  1. [Codebase](https://12factor.net/codebase): [GitHub-hosted repo](https://github.com/alexpovel/ancv/)\n  2. [Dependencies](https://12factor.net/dependencies): taken care of by [poetry](https://python-poetry.org/) and its standardized ([PEP 621](https://peps.python.org/pep-0621/)) [config](pyproject.toml) and [lock](poetry.lock) files, pinning all transient dependencies and providing virtual environments\n  3. [Config](https://12factor.net/config): the app is configured using environment variables.\n     Although [problematic](https://news.ycombinator.com/item?id=31200132), this approach was chosen for its simplicity\n  4. [Backing Services](https://12factor.net/backing-services): not applicable for this very simple app\n  5. [Build, release, run](https://12factor.net/build-release-run): handled through GitHub releases via git tags\n  6. [Processes](https://12factor.net/processes): this simple app is stateless in and of itself\n  7. [Port binding](https://12factor.net/port-binding): the `aiohttp` [server](ancv/web/server.py) part of the app acts as a [standalone web server](https://docs.aiohttp.org/en/stable/deployment.html#standalone), exposing a port.\n     That port can then be serviced by any arbitrary reverse proxy\n  8. [Concurrency](https://12factor.net/concurrency): covered by async functionality (in a single process and thread).\n     This being a stateless app, horizontal scaling through additional processes is trivial (e.g. via serverless hosting), although vertical scaling will likely suffice indefinitely\n  9. [Disposability](https://12factor.net/disposability): `aiohttp` handles `SIGTERM` gracefully\n  10. [Dev/prod parity](https://12factor.net/dev-prod-parity): trivial to do for this simple app.\n       If running on Windows, mind [this issue](https://stackoverflow.com/q/45600579/11477374).\n       If running on Linux, no special precautions are necessary\n  11. [Logs](https://12factor.net/logs): structural JSON logs are written directly to `stdout`\n  12. [Admin processes](https://12factor.net/admin-processes): not applicable either\n\n## Concept\n\n(put this as an SVG flowchart, left to right with conceptual sketches)\n\nSkeleton + Theme + Language + ASCII-mode toggle + Resume Data ==> terminal CV\n\n## Other solutions\n\nVery hard to find any, and even hard to google.\nFor example, `bash curl curriculum vitae` will prompt Google to interpret `curriculum vitae == resume`, which isn't wrong but `curl resume` is an entirely unrelated query (concerned with resuming halted downloads and such).\n\n- <https://github.com/soulshake/cv.soulshake.net>\n\nRelated, but 'fake' hits:\n\n- <https://ostechnix.com/create-beautiful-resumes-commandline-linux/>\n",
    'author': 'Alex Povel',
    'author_email': 'python@alexpovel.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ancv.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
