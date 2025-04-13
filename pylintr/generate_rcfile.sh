#!/usr/bin/env bash 

disables=''
good_names=''
disable=(
    "fixme"
    "broad-except"
    "too-few-public-methods"
    "too-many-arguments"
    "too-many-instance-attributes"
)
good_name=()
argument_rgx="^[a-z_][a-z0-9_]{0,30}$"
variable_rgx="^[a-z_][a-z0-9_]{0,30}$"

# Build string of items to disable.
for i in ${disable[@]}; do disables+="${i},"; done
for i in ${good_name[@]}; do good_names+="${i},"; done

# Generate a custom, project-specific config file.
pylint --reports=yes \
       --disable="${disables}" \
       --good-names="${good_names}" \
       --argument-rgx="${argument_rgx}" \
       --variable-rgx="${variable_rgx}" \
       --generate-rcfile > ../.pylintrc

