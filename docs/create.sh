#!/usr/bin/env bash

. ./.constants.config

printf "\nRemoving the current ./build directory ...\n"
rm -r $dirbuild
[ $? -eq 0 ] && printf "Done\n\n" || printf "Failed\n\n"

printf "Creating new docs ...\n"
sphinx-build $dirsource $dirbuild -b html

./spellcheck.sh

