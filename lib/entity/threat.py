from lib import Map
from .threat_category import ThreatCategory
from .threat_tag import ThreatTag

class Threat(Map):
    name: str
    categories: list[ThreatCategory]
    tags: list[ThreatTag]
