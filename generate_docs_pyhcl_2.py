#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import hcl
import hcl2
from lib.color import Bgcolor
from lib.parser import ColoredArgParser


class TFGenerator(object):
    TF_HEADER = """# Work with {0} via terraform

A terraform module for making {0}.


## Usage
----------------------
Import the module and retrieve with ```terraform get``` or \
```terraform get --update```. Adding a module resource to your template, e.g. \
`main.tf`:
"""

    INPUT_HEADER = "## Module Input Variables\n----------------------"
    OUTPUT_HEADER = "\n## Module Output Variables\n----------------------"
    AUTHORS = """

## Authors

Created and maintained by [Vitaliy Natarov](https://github.com/SebastianUA). \
An email: [vitaliy.natarov@yahoo.com](vitaliy.natarov@yahoo.com).

## License

Apache 2 Licensed. See [LICENSE]\
(https://github.com/SebastianUA/terraform/blob/master/LICENSE) for full details."""

    def __init__(self, m_dir, e_dir, hcl_version=1):
        self.m_dir, self.e_dir = m_dir, e_dir
        self.hcl_version = hcl_version
        self.parent_dir = self.get_parent_dir(m_dir)
        self.file_out = '{}/README.md'.format(self.e_dir)

    @classmethod
    def get_parent_dir(cls, path):
        return path.strip().split('/')[-1]

    def put_header(self):
        examples_file = os.path.join(self.e_dir, "main.tf")
        headers = self.TF_HEADER.format(self.parent_dir.upper())

        with open(self.file_out, 'w+') as f_out:
            f_out.write(headers + "\n")
            f_out.write("```\n")
            f_main = open(examples_file)
            f_out.writelines(f_main.readlines())
            f_out.write("\n```\n\n")

    def generate_inputs(self):
        tf_file_variables = os.path.join(self.m_dir, 'variables.tf')
        if not os.path.isfile(tf_file_variables):
            print(Bgcolor.fail('File doesnt exist! Check PATH to module!'))
            print(Bgcolor.fail("You're trying to use [{}]".format(self.m_dir)))
            raise ValueError()

        with open(self.file_out, 'a') as f_out:
            f_out.write(self.INPUT_HEADER + "\n")

        with open(tf_file_variables) as fp_in:
            try:
                if self.hcl_version == 1:
                    obj = hcl.load(fp_in)
                    for variable in obj['variable']:
                        description = obj['variable'][variable]['description'] or '""'
                        default = obj['variable'][variable]['default'] or '""'
                        if default is None:
                            default = 'null'
                        elif default == "":
                            default = '""'

                        line = '- `{}` - {} (`default = {}`)\n'.format(variable,
                                                                       description,
                                                                       default)
                        with open(self.file_out, 'a') as f_out:
                            f_out.write(line)
                else:
                    obj = hcl2.load(fp_in)
                    for section in obj['variable']:
                        # Dict contains only a single key, just take it
                        variable = next(iter(section))
                        description = section[variable]['description'][0] or '""'
                        default = section[variable]['default'][0]
                        if default is None:
                            default = 'null'
                        elif default == "":
                            default = '""'

                        line = '- `{}` - {} (`default = {}`)\n'.format(variable,
                                                                       description,
                                                                       default)
                        with open(self.file_out, 'a') as f_out:
                            f_out.write(line)
            except ValueError as err:
                print(Bgcolor.fail(err))

    def generate_outputs(self):
        tf_file_output = os.path.join(self.m_dir, 'outputs.tf')
        if os.path.isfile(tf_file_output):
            with open(self.file_out, 'a') as f_out:
                f_out.write(self.OUTPUT_HEADER + "\n")

        with open(tf_file_output) as fp_out:
            try:
                if self.hcl_version == 1:
                    obj = hcl.load(fp_out)
                    for output in obj['output']:
                        description = obj['output'][output]['description'] or '""'
                        line = '- `{}` - {}'.format(output, description)
                        with open(self.file_out, 'a') as f_out:
                            f_out.write(line + '\n')
                else:
                    obj = hcl2.load(fp_out)
                    for section in obj['output']:
                        # Dict contains only a single key, just take it
                        output = next(iter(section))
                        description = section[output]['description'][0] or '""'
                        line = '- `{}` - {}'.format(output, description)
                        with open(self.file_out, 'a') as f_out:
                            f_out.write(line + '\n')
            except ValueError as err:
                print(Bgcolor.fail(err))

    def put_footer(self):
        with open(self.file_out, 'a') as f_out:
            f_out.write(self.AUTHORS + "\n")

        print('The script ran from: {0}'.format(os.getcwd()))
        print('{0} has been created/updated'.format(self.file_out))

    def generate(self):
        self.put_header()
        self.generate_inputs()
        self.generate_outputs()
        self.put_footer()


def main():
    def dir_path(path):
        if os.path.isdir(path):
            return path
        raise ValueError("{} not a directory".format(path))

    parser = ColoredArgParser(prog='python3 script_name.py -h',
                              usage='python3 script_name.py {ARGS}',
                              add_help=True,
                              prefix_chars='--/',
                              epilog='''created by Vitalii Natarov''')
    parser.add_argument('--version', action='version', version='v1.1.0')
    parser.add_argument('-m', '--modules', dest='m_directory',
                        help='Set the directory where module exists',
                        metavar='DIR', type=dir_path, required=True)
    parser.add_argument('-e', '--examples', dest='e_directory',
                        help='Set the directory where example exists',
                        metavar='DIR', type=dir_path, required=True)
    parser.add_argument('--hcl-version', dest='hcl_version',
                        help='Set version of hcl to use for parsing terraform',
                        metavar='HCL VERSION', type=int, default=2, choices=[1, 2])
    args = parser.parse_args()

    tf_generator = TFGenerator(args.m_directory,
                               args.e_directory,
                               args.hcl_version)
    tf_generator.generate()

    print(Bgcolor.green("=" * 60))
    print(Bgcolor.green("=" * 25 + " FINISHED " + "=" * 25))
    print(Bgcolor.green("=" * 60))


if __name__ == '__main__':
    main()
