from lib import Map
from .url import URL
from .scan_result import ScanResult

class URLScanResult(ScanResult):
    url: URL
