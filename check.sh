#!/bin/bash
set -e

SOURCE_DIR="yamlfix"
TEST_DIR="tests"
MIN_COVERAGE=80

if [ ! "$(command -v black)" ] || [ ! "$(command -v flake8)" ] || [ ! "$(command -v shellcheck)" ] || [ ! "$(command -v yamllint)" ] || [ ! "$(command -v coverage)" ]; then
  ./install.sh
fi

echo "Entering Python-3 virtual environment..."
# shellcheck disable=SC1091
. .venv/bin/activate

echo "Checking code style with black"
black --check "$SOURCE_DIR" "$TEST_DIR"
echo

echo "Linting with flake8"
flake8 "$SOURCE_DIR" "$TEST_DIR"
echo

echo "Linting Shell scripts with shellcheck"
# shellcheck disable=SC2046
shellcheck ./*.sh $(find "$SOURCE_DIR" "$TEST_DIR" -iname "*.sh")
echo

echo "Linting YAML files with yamllint"
# shellcheck disable=SC2046
yamllint .yamllint $(find ./ -iname "*.y*ml")
echo

echo "Running unit tests"
coverage run --source="$SOURCE_DIR" -m unittest
echo

echo "Generating coverage report, check at least $MIN_COVERAGE% of the code is covered by the tests"
coverage report --fail-under="$MIN_COVERAGE"
echo
