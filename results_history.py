import os
import json
from datetime import datetime

PATH_FOLDER = 'history'


class ResultsHistory():
    def __init__(self, path=None):
        self.path = path or os.path.join(PATH_FOLDER, datetime.now().strftime('%Y-%m-%d') + ".json")

    def save(self, result):
        current = open(self.path, "w")
        current.write(json.dumps(result))
        current.close()
