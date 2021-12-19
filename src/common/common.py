import json

class Common:

    def __init__(self):
        self.load_conf()

    def load_conf(self):
        with open("../conf/conf.json", 'r') as f:
            self.conf = json.load(f)