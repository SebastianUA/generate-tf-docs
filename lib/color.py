class Bgcolor(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def _colored(cls, msg, color):
        return color + str(msg) + cls.ENDC

    @classmethod
    def header(cls, msg):
        return cls._colored(msg, cls.HEADER)

    @classmethod
    def blue(cls, msg):
        return cls._colored(msg, cls.OKBLUE)

    @classmethod
    def green(cls, msg):
        return cls._colored(msg, cls.OKGREEN)

    @classmethod
    def warning(cls, msg):
        return cls._colored(msg, cls.WARNING)

    @classmethod
    def fail(cls, msg):
        return cls._colored(msg, cls.FAIL)

    @classmethod
    def bold(cls, msg):
        return cls._colored(msg, cls.BOLD)

    @classmethod
    def underline(cls, msg):
        return cls._colored(msg, cls.UNDERLINE)
