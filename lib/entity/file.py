from lib import Map
from .threat import Threat
from .file_type import FileType

class File(Map):
    filename: str
    filepath: str
    path: str
    sha1: str
    sha256: str
    md5: str
    size: int
    type: str
    threat: Threat|None
    fileType: FileType|None
    id: int
