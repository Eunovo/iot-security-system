from genericpath import isfile
from os import path
from os import listdir, listdir
from os import path, makedirs
import time
import json


class CameraCtrl:
    def __init__(self, camera, captureDir):
        self.camera = camera
        self.captureDir = captureDir
        if not path.exists(captureDir):
            makedirs(captureDir)

    def capture(self):
        self.camera.capture(self.captureDir + 'Capture_' +
                            str(time.time()) + '.jpg')
        print('Captured an image')

    def listImages(self):
        files = listdir(self.captureDir)
        files = [f for f in files if path.isfile(path.join(self.captureDir, f))]
        return json.dumps(files)

    def readImage(self, filename):
        actual_path = path.join(self.captureDir, filename)
        if not path.exists(actual_path):
            raise ValueError(
                filename + ' does not exist in ' + self.captureDir)
        with open(actual_path, 'rb') as file:
            return file.read()
