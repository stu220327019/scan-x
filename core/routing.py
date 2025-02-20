from PySide6.QtCore import QObject, Signal
from lib import Map

class Route(Map):
    ROUTE_HOME = 0
    ROUTE_FILE_SCAN = 1
    ROUTE_URL_SCAN = 2
    ROUTE_THREATS = 3

    route: int
    params: dict

class Router(QObject):

    routeChanged = Signal(int, object)
    routeUpdated = Signal(object)

    _route = None

    def __init__(self):
        super().__init__()
        self.routeChanged.connect(self.updateRoute)

    def routeTo(self, routeId, routeParams = None):
        self.routeChanged.emit(routeId, routeParams)

    def updateRoute(self, routeId, routeParams):
        self._route = Route({
            'route': routeId,
            'params': routeParams
        })
        self.routeUpdated.emit(self._route)

    def getRoute(self):
        return self._route
