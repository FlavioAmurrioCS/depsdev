# depsdev

[![PyPI - Version](https://img.shields.io/pypi/v/depsdev.svg)](https://pypi.org/project/depsdev)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/depsdev.svg)](https://pypi.org/project/depsdev)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/FlavioAmurrioCS/depsdev/main.svg)](https://results.pre-commit.ci/latest/github/FlavioAmurrioCS/depsdev/main)

-----

## Table of Contents

- [depsdev](#depsdev)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Installation](#installation)
  - [CLI Usage](#cli-usage)
    - [Report mode](#report-mode)
  - [License](#license)

## Overview

Thin Python wrapper (async-first) around the public [deps.dev REST API](https://deps.dev) plus an optional Typer-based CLI. Provides straightforward methods mapping closely to the documented endpoints; responses are returned as decoded JSON (dict / list). Alpha endpoints can be enabled via `DEPSDEV_V3_ALPHA=true` and may change without notice.

## Installation

```bash
pip install depsdev            # library only
pipx install depsdev[cli]       # CLI
uv tool install depsdev[cli]       # CLI
```

## CLI Usage

```bash
[flavio@Mac ~/dev/github.com/FlavioAmurrioCS/depsdev][main ✗]
$ depsdev --help

 Usage: depsdev [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell.                                        │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation. │
│ --help                                                       Show this message and exit.                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ report   Show vulnerabilities for packages in a file.                                                                                           │
│ api      A CLI tool to interact with the https://docs.deps.dev/api/                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Utils ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ purl     Extract package URLs from various formats.                                                                                             │
│ vuln     Main function to analyze packages for vulnerabilities.                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Report mode

Parses depedency file and reports the vulnerabilities and the version where it was fixed.

```bash
[flavio@Mac ~/dev/github.com/FlavioAmurrioCS/depsdev][main ✗]
$ depsdev report --help

 Usage: depsdev report [OPTIONS] FILENAME

 Show vulnerabilities for packages in a file.

 Example usage:
 depsdev report requirements.txt
 depsdev report pom.xml
 depsdev report Pipfile.lock

╭─ Arguments ────────────────────────────────────────────────╮
│ *    filename      TEXT  [required]                        │
╰────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────╮
│ --help          Show this message and exit.                │
╰────────────────────────────────────────────────────────────╯

[flavio@Mac ~/dev/github.com/FlavioAmurrioCS/depsdev][main ✗]
$ uv export > requirements.txt
Resolved 34 packages in 6ms

[flavio@Mac ~/dev/github.com/FlavioAmurrioCS/depsdev][main ✗]
$ depsdev report requirements.txt
Analysing 10 packages...
Found 1 packages with advisories.
                                                                                      pkg:pypi/idna@3.6
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Id                  ┃ Summary                                                                                                                            ┃ Fixed                          ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ GHSA-jjg7-2v4v-x38h │ Internationalized Domain Names in Applications (IDNA) vulnerable to denial of service from specially crafted inputs to idna.encode │ 3.7                            │
│ PYSEC-2024-60       │                                                                                                                                    │ 1d365e17e10d72d0b7876316fc7b9… │
└─────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────────────────────────────┘
```

## License

`depsdev` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
