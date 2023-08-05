import xx_framework.conf.default_config as default_config
import json
import os

config_path = os.path.join(os.getcwd(), "config.json")
if os.path.isfile(config_path):
    print(f"loading config: {config_path}")
    with open("config.json", "r") as fp:
        user_config = json.load(fp)
else:
    user_config = {}


class LazyConfig:
    """配置懒加载，读取配置时，先读取用户自定义配置，没有则使用默认配置。"""

    def __getattr__(self, item):
        if user_config.__contains__(item):
            return user_config[item]
        elif hasattr(default_config, item):
            return getattr(default_config, item)
        return None


config = LazyConfig()

__ALL__ = [
    config
]
