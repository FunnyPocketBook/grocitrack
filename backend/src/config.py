import yaml
from pathlib import Path

config_dir = Path(__file__).parent.parent
config_path = config_dir / "config.yml"

class Config(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            cls.instance.load()
        return cls.instance

    def load(self):
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)

    def save(self, config):
        with open(config_path, "w") as f:
            yaml.dump(config, f)

    def get(self, key):
        return self._config[key]

    def set(self, key, value):
        self._config[key] = value
        self.save(self._config)