#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time
import hcl
import os
import os.path
import json


class Bgcolors:
    def __init__(self):
        self.get = {
            'HEADER': '\033[95m',
            'OKBLUE': '\033[94m',
            'OKGREEN': '\033[92m',
            'WARNING': '\033[93m',
            'FAIL': '\033[91m',
            'ENDC': '\033[0m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m'
        }


def header(m_dir, e_dir):
    if (m_dir is not None) and (e_dir is not None):
        dir_name = m_dir.strip().split('/')[-1]
        file_out = 'OUTPUT_{}.md'.format(dir_name)
        if os.path.isfile(file_out):
            os.remove(file_out)
        headers = """# Work with AWS {0} via terraform

A terraform module for making {0}.


## Usage
----------------------
Import the module and retrieve with ```terraform get``` or ```terraform get --update```. Adding a module resource to your template, e.g. `main.tf`:
""".format(dir_name.upper())

        examples_dir = "{0}".format(e_dir)
        examples_file = examples_dir + "/" + "main.tf"

        f_main = open(examples_file, "r")

        try:
            f = open(file_out, 'a')
            f.write(str(headers + "\n"))
            f.write("```\n")
            for x in f_main.readlines():
                f.write(x)
            f.write("```\n\n")
            f.close()
        except ValueError:
            print('I cant write to [{}] file'.format(file_out))

    else:
        print(Bgcolors().get['FAIL'], 'Please set/add [--mdir] or [--edir]', Bgcolors().get['ENDC'])
        print(Bgcolors().get['OKGREEN'], 'For help, use: script_name.py -h', Bgcolors().get['ENDC'])
        exit(1)

    return header


def generate_inputs(m_dir):
    if m_dir is not None:
        tf_file_variables = m_dir + '/' + 'variables.tf'
        if os.path.isfile(tf_file_variables) is False:
            print(Bgcolors().get['FAIL'], 'File doesnt exist! Check PATH to module!', Bgcolors().get['ENDC'])
            print(Bgcolors().get['FAIL'], "You're trying to use [{}]".format(dir), Bgcolors().get['ENDC'])
            exit(0)

        dir_name = m_dir.strip().split('/')[-1]
        file_out = 'OUTPUT_{}.md'.format(dir_name)

        input_header = """## Module Input Variables
----------------------"""

        try:
            f = open(file_out, 'a')
            f.write(str(input_header + "\n"))
            f.close()
        except ValueError:
            print('I cant write to [{}] file'.format(file_out))

        with open(tf_file_variables, 'r') as fp_in:
            obj = hcl.load(fp_in)
            # print (json.dumps(obj, indent=4, sort_keys=True))

            for variable in obj['variable']:
                description = obj['variable'][variable]['description']
                default = obj['variable'][variable]['default']

                line = '- `%s` - %s (`default = %s`)' % (str(variable), str(description), str(default))
                try:
                    f = open(file_out, 'a')
                    f.write(str(line + '\n'))
                    f.close()
                except ValueError:
                    print('I cant write to [{}] file'.format(file_out))

    else:
        print(Bgcolors().get['FAIL'], 'Please set/add [--mdir]', Bgcolors().get['ENDC'])
        print(Bgcolors().get['OKGREEN'], 'For help, use: script_name.py -h', Bgcolors().get['ENDC'])
        exit(1)

    return generate_inputs


def generate_outputs(m_dir):
    assert isinstance(m_dir, object)
    if m_dir is not None:
        tf_file_output = str(m_dir) + '/' + 'outputs.tf'
        dir_name = str(m_dir).split('/')[-1]
        file_out = 'OUTPUT_{}.md'.format(dir_name)
        if os.path.isfile(tf_file_output):
            # print(tf_file_output)
            output_header = """
            
## Module Output Variables
----------------------"""
            try:
                f = open(file_out, 'a')
                f.write(str(output_header + "\n"))
                f.close()
            except ValueError:
                print('I cant write to [{}] file'.format(file_out))

        with open(tf_file_output, 'r') as fp_out:
            obj = hcl.load(fp_out)
            # print (json.dumps(obj, indent=4, sort_keys=True))

            for output in obj['output']:
                description = obj['output'][output]['description']
                # print(description)
                if not description:
                    description = '""'

                line = '- `%s` - %s' % (output, description)
                try:
                    f = open(file_out, 'a')
                    f.write(str(line + '\n'))
                    f.close()
                except ValueError:
                    print('I cant write to [{}] file'.format(file_out))

    else:
        print(Bgcolors().get['FAIL'], 'Please set/add [--dir]', Bgcolors().get['ENDC'])
        print(Bgcolors().get['OKGREEN'], 'For help, use: script_name.py -h', Bgcolors().get['ENDC'])
        exit(1)

    return generate_outputs


def footer(m_dir):
    if m_dir is not None:
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

        try:
            f = open(file_out, 'a')
            f.write(str(authors + "\n"))
            f.close()
        except ValueError:
            print('I cant write to [{}] file'.format(file_out))

        print('Looks like that the [{0}] file has been created: {1}'.format(file_out, os.getcwd()))

    else:
        print(Bgcolors().get['FAIL'], 'Please set/add [--mdir]', Bgcolors().get['ENDC'])
        print(Bgcolors().get['OKGREEN'], 'For help, use: script_name.py -h', Bgcolors().get['ENDC'])
        exit(1)

    return footer


def main():
    start__time = time.time()
    parser = argparse.ArgumentParser(prog='python3 script_name.py -h',
                                     usage='python3 script_name.py {ARGS}',
                                     add_help=True,
                                     prefix_chars='--/',
                                     epilog='''created by Vitalii Natarov''')
    parser.add_argument('--version', action='version', version='v1.0.0')
    parser.add_argument('--md', '--mdir', dest='m_directory', help='Set the directory where module exists',
                        default=None, metavar='folder')
    parser.add_argument('--ed', '--edir', dest='e_directory', help='Set the directory where example exists',
                        default=None, metavar='folder')

    results = parser.parse_args()
    m_directory = results.m_directory  # type: object
    e_directory = results.e_directory

    header(m_directory, e_directory)
    generate_inputs(m_directory)
    generate_outputs(m_directory)
    footer(m_directory)

    end__time = round(time.time() - start__time, 2)
    print("--- %s seconds ---" % end__time)
    print(
        Bgcolors().get['OKGREEN'], "============================================================",
        Bgcolors().get['ENDC'])
    print(
        Bgcolors().get['OKGREEN'], "==========================FINISHED==========================",
        Bgcolors().get['ENDC'])
    print(
        Bgcolors().get['OKGREEN'], "============================================================",
        Bgcolors().get['ENDC'])


if __name__ == '__main__':
    main()
