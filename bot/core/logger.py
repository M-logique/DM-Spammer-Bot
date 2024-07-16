import logging as _logging

from colorlog import ColoredFormatter as _ColoredFormatter


class Logger(_logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(_logging.INFO)

        self.formatter = _ColoredFormatter(
            '%(asctime)s | %(log_color)s%(levelname)s%(reset)s | %(message)s',
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'cyan',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red',
                'SUCCESS':  'green'
            }
        )

        self.SUCCESS = 25
        _logging.addLevelName(self.SUCCESS, "SUCCESS") 

        self.success = lambda message: self._log(self.SUCCESS, message, (), extra={'color': 'green'})

        self.handler = _logging.StreamHandler()
        self.handler.setFormatter(self.formatter)
        self.addHandler(self.handler)

        self.info(f'{self.name} logger initialized.')