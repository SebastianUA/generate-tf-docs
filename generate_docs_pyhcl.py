#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import os.path
import json
import hcl
from lib.color import Bgcolor
from lib.parser import ColoredArgParser


def get_parent_dir(path):
    return path.strip().split('/')[-1]


def put_header(m_dir, e_dir):
    dir_name = get_parent_dir(m_dir)
    file_out = 'OUTPUT_{}.md'.format(dir_name)
    examples_file = os.path.join(e_dir, "main.tf")
    headers = """# Work with AWS {0} via terraform

A terraform module for making {0}.


## Usage
----------------------
Import the module and retrieve with ```terraform get``` or ```terraform get --update```. Adding a module resource to your template, e.g. `main.tf`:
""".format(dir_name.upper())

    with open(file_out, 'w+') as f:
        f.write(headers + "\n")
        f.write("```\n")
        f_main = open(examples_file)
        f.writelines(f_main.readlines())
        f.write("```\n\n")


def generate_inputs(m_dir):
    tf_file_variables = os.path.join(m_dir, 'variables.tf')
    if not os.path.isfile(tf_file_variables):
        print(Bgcolor.fail('File doesnt exist! Check PATH to module!'))
        print(Bgcolor.fail("You're trying to use [{}]".format(dir)))
        raise ValueError()

    dir_name = get_parent_dir(m_dir)
    file_out = 'OUTPUT_{}.md'.format(dir_name)
    input_header = """## Module Input Variables
----------------------"""

    with open(file_out, 'a') as f:
        f.write(input_header + "\n")

    with open(tf_file_variables) as fp_in:
        try:
            obj = hcl.load(fp_in)
            for variable in obj['variable']:
                description = obj['variable'][variable]['description']
                default = obj['variable'][variable]['default']
                line = '- `{}` - {} (`default = {}`)\n'.format(variable, description, default)
                with open(file_out, 'a') as f:
                    f.write(line)
        except ValueError as err:
            print(Bgcolor.fail(err))


def generate_outputs(m_dir):
    tf_file_output = os.path.join(m_dir, 'outputs.tf')
    dir_name = get_parent_dir(m_dir)
    file_out = 'OUTPUT_{}.md'.format(dir_name)
    if os.path.isfile(tf_file_output):
        output_header = """
        
## Module Output Variables
----------------------"""
        with open(file_out, 'a') as f:
            f.write(output_header + "\n")

    with open(tf_file_output) as fp_out:
        try:
            obj = hcl.load(fp_out)
            for output in obj['output']:
                description = obj['output'][output]['description'] or '""'
                line = '- `{}` - {}'.format(output, description)
                with open(file_out, 'a') as f:
                    f.write(line + '\n')
        except ValueError as err:
            print(Bgcolor.fail(err))


def put_footer(m_dir):
    dir_name = m_dir.strip().split('/')[-1]
    file_out = 'OUTPUT_{}.md'.format(dir_name)
    authors = """

## Authors
=======

Created and maintained by [Vitaliy Natarov](https://github.com/SebastianUA)
(vitaliy.natarov@yahoo.com).

License
=======

Apache 2 Licensed. See [LICENSE](https://github.com/SebastianUA/terraform/blob/master/LICENSE) for full details."""

    with open(file_out, 'a') as f:
        f.write(authors + "\n")

    print('"{0}" file has been created: {1}'.format(file_out, os.getcwd()))


def main():
    def dir_path(path):
        if os.path.isdir(path):
            return path
        raise ValueError("{} not a directory".format(path))

    start__time = time.time()
    parser = ColoredArgParser(prog='python3 script_name.py -h',
                              usage='python3 script_name.py {ARGS}',
                              add_help=True,
                              prefix_chars='--/',
                              epilog='''created by Vitalii Natarov''')
    parser.add_argument('--version', action='version', version='v1.0.0')
    parser.add_argument('-m', '--modules', dest='m_directory', help='Set the directory where module exists',
                        metavar='DIR', type=dir_path, required=True)
    parser.add_argument('-e', '--examples', dest='e_directory', help='Set the directory where example exists',
                        metavar='DIR', type=dir_path, required=True)

    results = parser.parse_args()
    m_directory = results.m_directory
    e_directory = results.e_directory

    put_header(m_directory, e_directory)
    generate_inputs(m_directory)
    generate_outputs(m_directory)
    put_footer(m_directory)

    end__time = round(time.time() - start__time, 2)
    print("--- %s seconds ---" % end__time)
    print(Bgcolor.green("=" * 60))
    print(Bgcolor.green("=" * 25 + " FINISHED " + "=" * 25))
    print(Bgcolor.green("=" * 60))


if __name__ == '__main__':
    main()
