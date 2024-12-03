import os

class SQLProvider:
    def __init__(self, path):
        self.scripts = {}
        for file in os.listdir(path):
            if file.endswith('.sql'):
                with open(f'{path}/{file}', 'r') as f:
                    self.scripts[file] = f.read()

    def get(self, name):
        if name not in self.scripts:
            raise ValueError(f'SQL template {name} not found')
        return self.scripts[name]
