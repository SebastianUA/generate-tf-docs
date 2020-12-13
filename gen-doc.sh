#!/usr/bin/env bash

PY_SCRIPT_PATH="/Users/captain/Projects/Python/generate-tf-docs/generate_docs_pyhcl.py"
TF_MODULES_PATH="/Users/captain/Projects/Terraform/aws/modules"
TF_EXAMPLES_PATH="/Users/captain/Projects/Terraform/aws/examples"

for folder in $(ls -lh /Users/captain/Projects/Terraform/aws/modules| grep '^d'| awk '{print $9}'| xargs -I{} -n1 echo {}); do
	echo "$folder"
	python3 ${PY_SCRIPT_PATH} -m="${TF_MODULES_PATH}/${folder}" -e="${TF_EXAMPLES_PATH}/${folder}"
done
