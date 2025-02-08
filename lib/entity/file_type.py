from lib import Map
from .file_type_tag import FileTypeTag

class FileType(Map):
    description: str
    extension: str
    tags: list[FileTypeTag]
