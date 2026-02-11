Yamlfix
==========

Yamlfix is a YAML formatter.

Prerequisites
-------------

- Linux or macOS
- [Python 3.6 or newer](https://www.python.org/downloads)

Installation
------------

```sh
./install.sh
```

Usage
-----

```sh
./run.sh
```

```
usage: yamlfix [-h] [-c] [-v | -l LOG_LEVEL] [path [path ...]]

Format YAML files

positional arguments:
  path                  Path to file or folder to format

optional arguments:
  -h, --help            show this help message and exit
  -c, --check           Do not reformat files, only check need for
                        reformatting. Returns an error code if a file needs to
                        be reformatted.
  -v, --verbose         Enable debug logging
  -l LOG_LEVEL, --log_level LOG_LEVEL
                        Enable a specific level of logging (1: DEBUG, 5:
                        CRITICAL, default: INFO)
```

### Examples

Format a single YAML file:
```sh
./run.sh config.yaml
```

Format all YAML files in a directory:
```sh
./run.sh ./config/
```

Check if files need reformatting without modifying them:
```sh
./run.sh --check config.yaml
```

Enable verbose logging:
```sh
./run.sh -v config.yaml
```

Tests and linting
-----------------

```sh
./check.sh
```