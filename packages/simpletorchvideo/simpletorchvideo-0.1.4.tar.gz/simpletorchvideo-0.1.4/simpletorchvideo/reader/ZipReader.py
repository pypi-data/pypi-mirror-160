import logging
import os
import zipfile
import cv2
import numpy as np

logger = logging.getLogger('base')


class ZipImageReader:
    def __init__(self, path: str):
        """Read data from zip
        :param path: path of the zip file
        """
        super().__init__()
        self.path = os.path.expanduser(path)
        assert self.valid(), "Not a valid ZipReader"
        self.file = None

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
        try:
            img_bytes = self.file.read(path)
        except zipfile.BadZipFile:
            self.file.close()
            logger.debug("Reopen zip file: %s" % self.path)
            self.file = zipfile.ZipFile(self.path, "r")
            img_bytes = self.file.read(path)
        return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    def _prepare_zip(self):
        if self.file is None:
            self.file = zipfile.ZipFile(self.path, "r")

    def list_images(self, path: str) -> [str]:
        """List a dir zip.
        :param path: path of the dir in zip
        :returns paths of the files in the dir, include sub dir
        """
        path = self._format_path(path)
        self._prepare_zip()
        return sorted(list(filter(lambda f: f[-1] != "/" and f.startswith(path), self.file.namelist())))

    def getinfo(self, path: str):
        self._prepare_zip()
        return self.file.getinfo(path)
