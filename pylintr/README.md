# pylintr
A simple Python script linting tool.

## Overview
This tool is wrapped around the `pylint` Python library, and simply iterates all `*.py` files in your project and generates a summary showing each module's score - highlighting the modules which fall below a score of 10/10.

## Usage

### Deployment and setup
When starting a new project:
1) Install `pylint` into your environment.
1) Copy the `pylintr` directory into the root of your project.
1) [Optional] Update the `generate_rcfile.sh` with the appropriate warnings to disable, and any name patterns to ignore.
1) Run `generate_rcfile.sh` to create the `.pylintrc` in the parent (typically project root) directory.

### Running
1) Navigate to the `pylintr` directory and run `./pylintr.sh`.
1) Once it's finished, review the output of the summary and fix (or disable) any warnings generated in your Python code.
