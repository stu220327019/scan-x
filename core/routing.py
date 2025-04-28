from PySide6.QtCore import QObject, Signal
from lib import Map

class Route(Map):
    ROUTE_HOME = 0
    ROUTE_FILE_SCAN = 1
    ROUTE_URL_SCAN = 2
    ROUTE_THREATS = 3
    ROUTE_FILES_SCANNED = 4

    route: int
    params: dict

class Router(QObject):

    routeChanged = Signal(int, object)
    routeUpdated = Signal(object)

    def __init__(self):
        super().__init__()
        self._routeState = list()
        self.routeChanged.connect(self.updateRoute)

    def routeTo(self, routeId, routeParams = None):
        self.routeChanged.emit(routeId, routeParams)

    def updateRoute(self, routeId, routeParams):
        route = Route({
            'route': routeId,
            'params': routeParams
        })
        self._routeState.append(route)
        self.routeUpdated.emit(route)

    def back(self):
        self._routeState.pop()
        self.routeUpdated.emit(self.getRoute())

    def getRoute(self):
        try:
            return self._routeState[-1]
        except IndexError:
            return None
