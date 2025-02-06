from lib import Map
from .file import File
from .scan_result import ScanResult

class FileScanResult(ScanResult):
    file: File
