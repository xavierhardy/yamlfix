#!/bin/sh
set -e

if [ ! "$(command -v yamlfix)" ]; then
  ./install.sh
fi

# shellcheck disable=SC2068
yamlfix $@
