import yaml

class Config(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            cls.instance.load()
        return cls.instance

    def load(self):
        with open("config.yml", "r") as f:
            self._config = yaml.safe_load(f)

    def save(self, config):
        with open("config.yml", "w") as f:
            yaml.dump(config, f)

    def get(self, key):
        return self._config[key]

    def set(self, key, value):
        self._config[key] = value
        self.save(self._config)