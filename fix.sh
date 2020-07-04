#!/bin/bash
set -e

SOURCE_DIR="yamlfix"
TEST_DIR="tests"

if [ ! "$(command -v black)" ] || [ ! "$(command -v flake8)" ] || [ ! "$(command -v shellcheck)" ] || [ ! "$(command -v yamllint)" ] || [ ! "$(command -v coverage)" ]; then
  ./install.sh
fi

echo "Entering Python-3 virtual environment..."
# shellcheck disable=SC1091
. .venv/bin/activate

echo "Checking code style with black"
black "$SOURCE_DIR" "$TEST_DIR"
echo
