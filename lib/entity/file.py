from lib import Map

class File(Map):
    STATUS_PENDING = 'Pending'
    STATUS_QUEUED = 'Queued'
    STATUS_SCANNING = 'Scanning'
    STATUS_COMPLETED = 'Completed'
    STATUS_ATTENTION = 'Attention'
    STATUS_INFECTED = 'Virus detected ({})'
    STATUS_FAILED = 'Failed: {}'
    STATUS_CANCELED = 'Canceled'
    STATUS_CLEAN = 'Clean'

    filename: str
    filepath: str
    path: str
    sha1: str
    sha256: str
    md5: str
    size: int
    type: str
    status: str
