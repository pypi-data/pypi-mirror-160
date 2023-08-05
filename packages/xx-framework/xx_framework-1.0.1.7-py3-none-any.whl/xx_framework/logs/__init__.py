import logging
import os
import random
import time

from xx_framework.conf import config

log_config = config.LOGS


class MyLog:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            setattr(cls, "_instance", super(MyLog, cls).__new__(cls))
        return getattr(cls, "_instance")

    def __init__(self, name="xx_framework", set_file=log_config['file_log'], set_console=log_config['stream_log']):
        name = f"_{name}" if name else ''
        date_str = time.strftime("%Y%m%d")
        file_name = f"{date_str}{name}.log"
        # 创建logger
        self.logger = logging.getLogger(f"{file_name}_{random.randint(1000, 10000)}")
        # 设置logger开关
        self.logger.setLevel(logging.DEBUG)

        if set_file:
            if not os.path.isdir(log_config['my_log_dir']):
                os.mkdir(log_config['my_log_dir'])
            # 创建写入文件的handler
            file_handler = logging.FileHandler(os.path.join(log_config['my_log_dir'], file_name), mode='a',
                                               encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"))
            self.logger.addHandler(file_handler)

        if set_console:
            # 创建写入控制台的handler
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(stream_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
