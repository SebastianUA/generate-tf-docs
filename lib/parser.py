import argparse
import sys
from lib.color import Bgcolor


class ColoredArgParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None, color=None):
        if message:
            if file is None:
                file = sys.stderr
            if color is None:
                file.write(message)
            else:
                # \x1b[ is the ANSI Control Sequence Introducer (CSI)
                file.write(color + message.strip() + Bgcolor.ENDC + "\n")

    def print_usage(self, file=None):
        if file is None:
            file = sys.stdout
        self._print_message(self.format_usage()[0].upper() +
                            self.format_usage()[1:],
                            file)

    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        self._print_message(self.format_help()[0].upper() +
                            self.format_help()[1:],
                            file,
                            Bgcolor.OKBLUE)

    def exit(self, status=0, message=None):
        if status == 0:
            self._print_message(message, sys.stdout, Bgcolor.OKGREEN)
        else:
            self._print_message(message, sys.stderr, Bgcolor.FAIL)
        sys.exit(status)

    def error(self, message):
        self.print_usage(sys.stderr)
        args = {'prog' : self.prog, 'msg': message}
        self.exit(2, '{prog}: Error: {msg}\n'.format(**args))
