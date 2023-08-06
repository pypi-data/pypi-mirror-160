import json
import os
from datetime import date, datetime


class FileManager:

    def __init__ (self, base_path=None):

        self.dir = {}
        if os.name == 'nt':
            self.sep = '\\'
            if base_path == None:
                base_path = os.getenv('APPDATA') + '\\trisigma\\'

        elif os.name == 'posix':
            self.sep = '/'
            if base_path == None:
                base_path = '/var/lib/trisigma/'
        else:
            print(f'OS not supported: {os.name}')
            return None

        self.__setup(base_path)

    def __setup (self, base_path):
        self.dir['base'] = base_path
        self.dir['log'] = self.dir['base'] + f'log{self.sep}'
        self.dir['data'] = self.dir['base'] + f'data{self.sep}'
        self.dir['config'] = self.dir['base'] + f'config{self.sep}'
        self.dir['var'] = self.dir['data'] + f'var{self.sep}'
        self.dir['plot'] = self.dir['data'] + f'plot{self.sep}'
        [self.__mkdir(dir) for dir in self.dir.values()]

    def __mkdir (self,dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    def log(self, name, data):
        with open(self.dir['log'] + name + '.txt', 'a') as file:
            file.write(self.get_time() + '\t' + str(data) + '\n')

    def save(self, output, name):
        with open(self.dir['var'] + name + '.json', 'w') as file:
            json.dump(output, file)

    def load(self, name):
        with open(self.dir['var'] + name + '.json', 'r') as file:
            var = json.load(file)
            return var

    def append(self, item, name):
        var = self.load(name)
        if isinstance(var, list):
            var.append(item)
            self.save(var, name)
            return var
        else:
            return print('err, there is no list in here.')

    def get_time(self):
        return str(datetime.now())

    def key(self,file):
        global config
        return config[file]

