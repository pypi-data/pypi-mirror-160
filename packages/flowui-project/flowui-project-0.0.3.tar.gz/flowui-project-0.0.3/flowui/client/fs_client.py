from pathlib import Path
from botocore.exceptions import ClientError
from flowui.logger import get_configured_logger


class FSClient(object):
    def __init__(self):
        self.logger = get_configured_logger(self.__class__.__name__)

    def create_fs_results_path(self, results_path_fs):
        """Creates File System dir for task run results"""
        try:
            filepath = Path(results_path_fs)
            filepath.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.exception(e)
