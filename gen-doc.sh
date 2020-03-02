#!/usr/bin/env bash

for folder in $(ls -lh /Users/captain/Projects/Terraform/aws/modules| grep '^d'| awk '{print $9}'| xargs -I{} -n1 echo {}); do
	echo "$folder"
	python3 /Users/captain/Projects/Python/Terraform/generate_docs_pyhcl.py --mdir="/Users/captain/Projects/Terraform/aws/modules/${folder}" --edir="/Users/captain/Projects/Terraform/aws/examples/${folder}"
done