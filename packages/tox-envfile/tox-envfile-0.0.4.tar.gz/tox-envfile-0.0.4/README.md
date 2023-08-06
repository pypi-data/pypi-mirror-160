<a href="https://github.com/hypothesis/tox-envfile/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/workflow/status/hypothesis/tox-envfile/CI/main"></a>
<a href="https://pypi.org/project/tox-envfile"><img src="https://img.shields.io/pypi/v/tox-envfile"></a>
<a><img src="https://img.shields.io/badge/python-3.10 | 3.9 | 3.8-success"></a>
<a href="https://github.com/hypothesis/tox-envfile/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# tox-envfile

Load env files in your tox envs.

For installation instructions see [INSTALL.md](https://github.com/hypothesis/tox-envfile/blob/main/INSTALL.md).

For how to set up a tox-envfile development environment see
[HACKING.md](https://github.com/hypothesis/tox-envfile/blob/main/HACKING.md).

tox-envfile reads environment variables from a file named `.devdata.env` in the
same directory as your `tox.ini` file and adds them to the environment that tox
runs your commands in.

This is a pretty dumb plugin for now: all of the environment variables in
`.devdata.env` will be loaded into the environment for every tox env that you
run, unconditionally. Any existing envvars with conflicting names will be
overwritten. Only a single environment file is supported and it must be named
`.devdata.env`.

env File Format
---------------

[python-dotenv](https://saurabh-kumar.com/python-dotenv/) is used for the env file parsing.

The `.devdata.env` file should be an env file with contents that look like
this:

```shell
# a comment that will be ignored.
REDIS_ADDRESS=localhost:6379
MEANING_OF_LIFE=42
MULTILINE_VAR="hello\nworld"
```

Or like this:

```shell
export S3_BUCKET=YOURS3BUCKET
export SECRET_KEY=YOURSECRETKEYGOESHERE
```

POSIX variable expansion works, using variables from the environment or from
earlier lines in the env file:

```shell
CONFIG_PATH=${HOME}/.config/foo
DOMAIN=example.org
EMAIL=admin@${DOMAIN}
```
