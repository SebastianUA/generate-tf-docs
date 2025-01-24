#!/usr/bin/env bash

PY_SCRIPT_PATH="/Users/captain/Workshop/Python/generate-tf-docs/generate_docs_pyhcl_2.py"
TF_MODULES_PATH="/Users/captain/Workshop/Terraform/$1/modules"
TF_EXAMPLES_PATH="/Users/captain/Workshop/Terraform/$1/examples"

for folder in $(ls -lh /Users/captain/Workshop/Terraform/$1/modules| grep '^d'| awk '{print $9}'| xargs -I{} -n1 echo {}); do
	echo "folder: ${folder}"
	python3 "${PY_SCRIPT_PATH}" -m="${TF_MODULES_PATH}/${folder}" -e="${TF_EXAMPLES_PATH}/${folder}"
done
