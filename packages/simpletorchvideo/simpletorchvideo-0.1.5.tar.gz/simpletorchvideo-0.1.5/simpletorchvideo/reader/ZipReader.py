import logging
import os
import zipfile
import cv2
import numpy as np

logger = logging.getLogger('base')

global_zipfiles = {}


class ZipImageReader:
    def __init__(self, path: str):
        """Read data from zip
        :param path: path of the zip file
        """
        super().__init__()
        self.path = os.path.expanduser(path)
        assert self.valid(), "Not a valid ZipReader"

    def valid(self) -> bool:
        return zipfile.is_zipfile(self.path)

    @staticmethod
    def _format_path(path):
        path = path.replace("\\", "/")
        path = path[1:] if path[0] == "/" else path
        path = path[0:-1] if path[-1] == "/" else path
        return path

    def read_image(self, path: str):
        """Read a file from a zip.
        :param path: path of the file in zip
        :returns buffer-like file content
        """
        path = self._format_path(path)
        self._prepare_zip()
        try:
            img_bytes = global_zipfiles[self.path].read(path)
        except zipfile.BadZipFile:
            global_zipfiles[self.path].close()
            logger.debug("Reopen zip file: %s" % self.path)
            global_zipfiles[self.path] = zipfile.ZipFile(self.path, "r")
            img_bytes = global_zipfiles[self.path].read(path)
        return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    def _prepare_zip(self):
        if self.path not in global_zipfiles or global_zipfiles[self.path] is None:
            global_zipfiles[self.path] = zipfile.ZipFile(self.path, "r")

    def list_images(self, path: str) -> [str]:
        """List a dir zip.
        :param path: path of the dir in zip
        :returns paths of the files in the dir, include sub dir
        """
        path = self._format_path(path)
        self._prepare_zip()
        return sorted(list(
            filter(lambda f: f[-1] != "/" and f.startswith(path), global_zipfiles[self.path].namelist())
        ))

    def getinfo(self, path: str):
        self._prepare_zip()
        return global_zipfiles[self.path].getinfo(path)
