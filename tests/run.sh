#!/usr/bin/env bash

export PYTHONPATH=$( realpath .. )

printf "\nRunning unit tests ..."
python -m unittest discover
printf "\nTesting complete.\n\n"

