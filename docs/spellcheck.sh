#!/usr/bin/env bash

. ./.constants.config

printf "\nChecking documentation spelling.\n"

printf "\nCleaning up from the previous run ...\n"
if ls $files_spelling > /dev/null 2>&1; then
    for f in ${files_spelling[@]}; do
        printf "<> Deleting %s\n" $f
        rm $f
    done
    printf "Done.\n\n"
else
    printf "No files to remove.\n\n"
fi

# Run spell checker.
sphinx-build $dirsource $dirbuild -b spelling

# Redefine spelling files array.
files_spelling=( $dirbuild/*.spelling ) 
printf "\nSummary:\n----------\n"
if ls $files_spelling > /dev/null 2>&1; then
    cat $dirbuild/*.spelling
else
    printf "No spelling errors found.\n"
fi

printf "\nDone.\n\n"

