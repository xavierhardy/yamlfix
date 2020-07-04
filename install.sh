#!/bin/sh
set -e

if [ ! "$(command -v shellcheck)" ]; then
  echo "Shellcheck is missing, install it: https://github.com/koalaman/shellcheck#installing"
  exit 1
fi

if [ ! "$(command -v python3)" ]; then
  echo "Python 3 is missing, install it: https://www.python.org/downloads"
  exit 1
fi

if [ ! "$(command -v pip)" ]; then
  echo "Downloading and installing pip..."
  curl -sSL https://bootstrap.pypa.io/get-pip.py | python
fi

if [ ! "$(command -v virtualenv)" ]; then
  echo "Downloading and installing virtualenv..."
  pip install virtualenv
fi

if [ ! -d .venv ]; then
  echo "Creating Python-3 virtual environment..."
  virtualenv -p python3 .venv
fi

echo "Entering Python-3 virtual environment..."
# shellcheck disable=SC1091
. .venv/bin/activate

if [ ! "$(command -v poetry)" ]; then
  echo "Downloading and installing peotry..."
  pip install poetry
fi

echo "Installing project..."
poetry install
