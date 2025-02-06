from lib import Map
from .analysis import Analysis

class ScanResult(Map):
    STATUS_PENDING = 'Pending'
    STATUS_QUEUED = 'Queued'
    STATUS_SCANNING = 'Scanning'
    STATUS_COMPLETED = 'Completed'
    STATUS_ATTENTION = 'Attention'
    STATUS_INFECTED = 'Virus detected ({})'
    STATUS_FAILED = 'Failed: {}'
    STATUS_CANCELED = 'Canceled'
    STATUS_CLEAN = 'Clean'

    analysis: Analysis
    clean: bool
    startedTime: int
    finishedTime: int
    scannedAt: int
    status: str
    id: str
